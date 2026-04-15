from __future__ import annotations

import json
from typing import Dict, List

from assistant_app.contracts import MemoryFact
from assistant_app.memory.store import MemoryStore


ALLOWED_POLICY_TYPES = {"global", "task", "tool_source"}


ALLOWED_MEMORY_TYPES = {
    "user_identity",
    "catalog_seen",
    "temporary_preference",
    "durable_preference",
    "personal_context",
    "goal",
    "constraint",
}


class TurnReflectionExtractor:
    def __init__(self, provider) -> None:
        self.provider = provider

    def extract(self, user_text: str, assistant_text: str, active_policies: List[Dict], recent_history: List[Dict]) -> Dict[str, List]:
        active_policy_lines = json.dumps(active_policies, ensure_ascii=False)
        recent_history_lines = json.dumps(recent_history, ensure_ascii=False)
        prompt = f"""
Analyze the conversation turn and extract:
1. memory_facts: memories likely useful in future conversations
2. policies: persistent behavioral policies that should guide future behavior

Return valid JSON only.

Rules for memory_facts:
- Use only explicit user statements or clearly confirmed facts.
- Use the recent conversation history to detect corrections, replacements, and contradictions.
- If the user corrects a previously stated identity fact, output only the corrected fact, not both versions.
- Temporary wishes like "today I don't want romance" must be `temporary_preference`.
- Stable facts like name, recurring preferences, constraints, or goals can use other memory types.
- Write `summary` in Brazilian Portuguese.
- Use `subject = "given_name"` when the user only states their name, like "me chamo X" or "meu nome é X".
- Use `subject = "preferred_name"` only when the user explicitly says how they prefer to be called.

Allowed memory_type values:
- user_identity
- catalog_seen
- temporary_preference
- durable_preference
- personal_context
- goal
- constraint

Rules for policies:
- Save only explicit operating instructions from the user.
- Use the recent conversation history to understand whether the user is refining an existing instruction or adding a new independent one.
- Policy types: global, task, tool_source
- For greetings or wording rules, prefer global.
- For source preference like MDL or Reddit, prefer tool_source.
- `applies_to` may include arrays: intent_tags, domain_tags, tool_tags, source_tags, phase_tags, text_triggers
- Include `policy_slot`, a short stable identifier for the policy family.
- Include `operation` with one of: `set`, `replace`, `deactivate`, `downgrade`.
- If the user refines or corrects an existing rule, reuse the same `policy_slot` and prefer `replace`.
- If the user adds a different instruction that can coexist with the previous one, create a different `policy_slot`.
- Do not collapse two independent user instructions into one slot just because both are `global`.

Current active policies:
{active_policy_lines}

Recent conversation history:
{recent_history_lines}

JSON schema:
{{
  "memory_facts": [
    {{
      "memory_type": "user_identity",
      "subject": "given_name",
      "summary": "O nome do usuário é Gean.",
      "value": {{"given_name": "Gean"}},
      "confidence": 0.98,
      "temporal_weight": 1.0,
      "temporary_hours": null
    }}
  ],
  "policies": [
    {{
      "policy_type": "global",
      "policy_slot": "response_opening_style",
      "operation": "set",
      "instruction": "Use uma abertura mais calorosa quando fizer sentido.",
      "priority": 0.95,
      "active": true,
      "applies_to": {{}}
    }}
  ]
}}

Conversation turn:
User: {user_text}
Assistant: {assistant_text}
""".strip()
        raw = self.provider.complete_text("Return JSON only.", prompt)
        parsed = self._parse_json(raw)
        policies = self._merge_with_active_policies(
            parsed_policies=self._parse_policies(parsed.get("policies")),
            user_text=user_text,
            active_policies=active_policies,
        )
        return {
            "memory_facts": self._parse_memory_facts(parsed.get("memory_facts")),
            "policies": policies,
            "raw": raw,
        }

    def _parse_memory_facts(self, payload) -> List[MemoryFact]:
        if not isinstance(payload, list):
            return []
        facts: List[MemoryFact] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            memory_type = str(item.get("memory_type", "")).strip()
            subject = str(item.get("subject", "")).strip()
            summary = str(item.get("summary", "")).strip()
            value = item.get("value")
            if memory_type not in ALLOWED_MEMORY_TYPES or not subject or not isinstance(value, dict):
                continue
            if summary and "summary" not in value:
                value = {**value, "summary": summary}
            expires_at = None
            if memory_type == "temporary_preference":
                hours = item.get("temporary_hours")
                if not isinstance(hours, int) or hours <= 0:
                    hours = 24
                expires_at = MemoryStore.temporary_expiry(hours)
            facts.append(
                MemoryFact(
                    memory_type=memory_type,
                    subject=subject[:120],
                    value=value,
                    confidence=self._clamp(item.get("confidence"), 0.75),
                    temporal_weight=self._clamp(item.get("temporal_weight"), 0.75),
                    source="reflection",
                    expires_at=expires_at,
                )
            )
        return facts

    def _parse_policies(self, payload) -> List[Dict]:
        if not isinstance(payload, list):
            return []
        items: List[Dict] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            policy_type = str(item.get("policy_type", "")).strip()
            policy_slot = str(item.get("policy_slot", "")).strip()
            operation = str(item.get("operation", "set")).strip().lower() or "set"
            instruction = str(item.get("instruction", "")).strip()
            applies_to = item.get("applies_to") or {}
            if (
                policy_type not in ALLOWED_POLICY_TYPES
                or not policy_slot
                or operation not in {"set", "replace", "deactivate", "downgrade"}
                or (operation != "deactivate" and not instruction)
                or not isinstance(applies_to, dict)
            ):
                continue
            items.append(
                {
                    "policy_type": policy_type,
                    "policy_slot": policy_slot,
                    "operation": operation,
                    "instruction": instruction,
                    "priority": self._clamp(item.get("priority"), 0.85),
                    "active": bool(item.get("active", True)),
                    "applies_to": self._normalize_applies_to(applies_to),
                    "source": "reflection",
                }
            )
        return items

    def _merge_with_active_policies(self, parsed_policies: List[Dict], user_text: str, active_policies: List[Dict]) -> List[Dict]:
        if not parsed_policies:
            return []
        existing_by_slot = {
            str(item.get("policy_slot", "")).strip().lower(): item
            for item in active_policies
            if str(item.get("policy_slot", "")).strip()
        }
        merged: List[Dict] = []
        for policy in parsed_policies:
            slot = policy["policy_slot"].strip().lower()
            previous = existing_by_slot.get(slot)
            if policy.get("operation") != "replace" or not previous:
                merged.append(policy)
                continue
            merged_instruction = self._merge_policy_instruction(
                previous_instruction=str(previous.get("instruction", "")).strip(),
                revised_instruction=str(policy.get("instruction", "")).strip(),
                user_text=user_text,
            )
            if merged_instruction:
                policy = {**policy, "instruction": merged_instruction}
            merged.append(policy)
        return merged

    def _merge_policy_instruction(self, previous_instruction: str, revised_instruction: str, user_text: str) -> str:
        if not previous_instruction or not revised_instruction:
            return revised_instruction or previous_instruction
        prompt = f"""
You are revising a persistent user instruction.

Goal:
- produce one merged instruction in Brazilian Portuguese
- preserve still-valid constraints from the previous instruction
- incorporate the user's new refinement
- remove prior parts only if the user clearly revoked or contradicted them
- preserve explicit negative constraints, prohibitions, exclusions, replacements, and avoid/unless clauses from the previous instruction unless the user clearly revoked them
- if the previous instruction said to avoid or replace something, keep that avoidance or replacement in the merged result unless the user explicitly changed it
- keep the result concise and natural

Return plain text only.

Previous instruction:
{previous_instruction}

User refinement:
{user_text}

Draft revised instruction:
{revised_instruction}
""".strip()
        merged = self.provider.complete_text("Return one merged instruction in Brazilian Portuguese. Plain text only.", prompt).strip()
        return merged or revised_instruction

    @staticmethod
    def _parse_json(raw: str):
        text = raw.strip()
        if not text:
            return {}
        try:
            parsed = json.loads(text)
            return parsed if isinstance(parsed, dict) else {}
        except json.JSONDecodeError:
            pass
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                parsed = json.loads(text[start : end + 1])
                return parsed if isinstance(parsed, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}

    @staticmethod
    def _clamp(value, default: float) -> float:
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return default
        return max(0.0, min(1.0, parsed))

    @staticmethod
    def _normalize_applies_to(applies_to: Dict) -> Dict:
        normalized: Dict[str, List[str]] = {}
        for key in ("intent_tags", "domain_tags", "tool_tags", "source_tags", "phase_tags", "text_triggers"):
            values = applies_to.get(key) or []
            if not isinstance(values, list):
                continue
            cleaned = []
            seen = set()
            for value in values:
                text = str(value).strip().lower()
                if not text or text in seen:
                    continue
                seen.add(text)
                cleaned.append(text)
            if cleaned:
                normalized[key] = cleaned
        phase_tags = normalized.get("phase_tags") or []
        if "response_opening" in phase_tags and "greeting" not in phase_tags:
            normalized["phase_tags"] = [*phase_tags, "greeting"]
        return normalized
