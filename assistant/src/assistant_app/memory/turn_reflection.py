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

    def extract(
        self,
        user_text: str,
        assistant_text: str,
        active_policies: List[Dict],
        recent_history: List[Dict],
        memory_profile: Dict,
        profile_source_entries: List[Dict],
    ) -> Dict:
        active_policy_lines = json.dumps(active_policies, ensure_ascii=False)
        recent_history_lines = json.dumps(recent_history, ensure_ascii=False)
        profile_lines = json.dumps(memory_profile, ensure_ascii=False)
        source_entry_lines = json.dumps(self._format_profile_source_entries(profile_source_entries), ensure_ascii=False)
        prompt = f"""
Analyze the conversation turn and extract:
1. memory_facts: memories likely useful in future conversations
2. memory_operations: explicit cleanup operations for old memory records
3. policies: persistent behavioral policies that should guide future behavior
4. profile_text: the consolidated user memory profile

Return valid JSON only.

Rules for memory_facts:
- Use only explicit user statements or clearly confirmed facts.
- Use the recent conversation history to detect corrections, replacements, and contradictions.
- If the user corrects a previously stated identity fact, output only the corrected fact, not both versions.
- Include `operation` with one of: `set`, `replace`.
- Use `replace` when the latest user message changes or corrects a previous memory on the same topic.
- When using `replace`, write the new fact as the current truth, not as a note that a change happened.
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

Rules for memory_operations:
- Use this to remove stale or contradicted entries from "All active memory records".
- Return `supersede` for memory records that should no longer be considered active because the latest turn replaced, corrected, or contradicted them.
- Include the exact `item_key` from "All active memory records".
- Do not supersede stable non-conflicting memories.
- If the new memory replaces older memories with different subjects but the same real-world topic, supersede those older item_keys.
- If no cleanup is needed, return an empty array.

Rules for policies:
- Save only explicit operating instructions from the user.
- Use the recent conversation history to understand whether the user is refining an existing instruction or adding a new independent one.
- Preserve still-valid constraints from an existing policy when the user refines it.
- Remove prior policy parts only if the user clearly revoked or contradicted them.
- Preserve explicit negative constraints, prohibitions, exclusions, replacements, and avoid/unless clauses unless clearly revoked.
- If a current active policy is contradicted and should not guide future behavior, return that policy_slot with `operation = "deactivate"`.
- Policy types: global, task, tool_source
- For greetings or wording rules, prefer global.
- For source preference like MDL or Reddit, prefer tool_source.
- `applies_to` may include arrays: intent_tags, domain_tags, tool_tags, source_tags, phase_tags, text_triggers
- Include `policy_slot`, a short stable identifier for the policy family.
- Include `operation` with one of: `set`, `replace`, `deactivate`, `downgrade`.
- If the user refines or corrects an existing rule, reuse the same `policy_slot` and prefer `replace`.
- If the user adds a different instruction that can coexist with the previous one, create a different `policy_slot`.
- Do not collapse two independent user instructions into one slot just because both are `global`.

Rules for profile_text:
- Rebuild the consolidated user memory profile in Brazilian Portuguese.
- Use short bullet points.
- Preserve stable non-conflicting preferences.
- Include corrected facts from this latest turn.
- If memories conflict, the newest evidence wins.
- The latest conversation turn is the newest evidence.
- Remove or rewrite older profile statements contradicted by the latest turn.
- Do not mention timestamps.
- If there is no useful memory, return "Nenhuma memória consolidada ainda."

Current active policies:
{active_policy_lines}

Current consolidated memory profile:
{profile_lines}

All active memory records, oldest to newest:
{source_entry_lines}

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
      "operation": "set",
      "temporary_hours": null
    }}
  ],
  "memory_operations": [
    {{
      "operation": "supersede",
      "item_key": "candidate:abc123",
      "reason": "Foi substituída por uma preferência mais recente."
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
  ],
  "profile_text": "- O nome do usuário é Gean.\\n- O usuário prefere respostas curtas."
}}

Conversation turn:
User: {user_text}
Assistant: {assistant_text}
""".strip()
        raw = self.provider.complete_text("Return JSON only.", prompt)
        parsed = self._parse_json(raw)
        return {
            "memory_facts": self._parse_memory_facts(parsed.get("memory_facts")),
            "memory_operations": self._parse_memory_operations(parsed.get("memory_operations")),
            "policies": self._parse_policies(parsed.get("policies")),
            "profile_text": self._parse_profile_text(parsed.get("profile_text")),
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
            operation = str(item.get("operation", "set")).strip().lower() or "set"
            if operation not in {"set", "replace"}:
                operation = "set"
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
                    operation=operation,
                    source="reflection",
                    expires_at=expires_at,
                )
            )
        return facts

    def _parse_memory_operations(self, payload) -> List[Dict]:
        if not isinstance(payload, list):
            return []
        items: List[Dict] = []
        for item in payload:
            if not isinstance(item, dict):
                continue
            operation = str(item.get("operation", "")).strip().lower()
            item_key = str(item.get("item_key", "")).strip()
            reason = str(item.get("reason", "")).strip()
            if operation != "supersede" or not item_key:
                continue
            if not (item_key.startswith("candidate:") or item_key.startswith("durable:")):
                continue
            items.append(
                {
                    "operation": operation,
                    "item_key": item_key,
                    "reason": reason,
                }
            )
        return items

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

    @staticmethod
    def _parse_profile_text(payload) -> str:
        if not isinstance(payload, str):
            return ""
        return payload.strip()

    @staticmethod
    def _format_profile_source_entries(entries: List[Dict]) -> List[Dict]:
        formatted = []
        for item in entries:
            value = item.get("value") or {}
            formatted.append(
                {
                    "kind": item.get("kind"),
                    "item_key": item.get("item_key"),
                    "source_ref": item.get("source_ref"),
                    "updated_at": item.get("updated_at"),
                    "memory_type": item.get("memory_type"),
                    "subject": item.get("subject"),
                    "summary": value.get("summary") or value,
                }
            )
        return formatted

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
