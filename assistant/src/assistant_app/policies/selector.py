from __future__ import annotations

import json
from typing import Dict, List


class PolicySelector:
    def __init__(self, provider) -> None:
        self.provider = provider

    def select_for_turn(self, message_text: str, policies: List[Dict]) -> List[Dict]:
        if not policies:
            return []
        payload = [
            {
                "policy_slot": item.get("policy_slot", ""),
                "policy_type": item.get("policy_type", ""),
                "instruction": item.get("instruction", ""),
                "applies_to": item.get("applies_to") or {},
                "priority": item.get("priority", 0.0),
            }
            for item in policies
        ]
        prompt = f"""
Select which stored policies are genuinely applicable to the current user message.

Rules:
- Return JSON only.
- Default to no policies.
- Choose only policies that are clearly needed for this specific reply.
- If none are clearly needed, return an empty list.
- Never choose a policy just because it exists.
- Prefer at most one policy for a normal conversational reply.
- Use the policy metadata too.
- If `applies_to.phase_tags` includes `greeting` or `response_opening`, the policy can apply to a greeting or conversational opening, but not to acknowledgements or ordinary follow-up questions.

Current user message:
{message_text}

Candidate policies:
{json.dumps(payload, ensure_ascii=False)}

JSON schema:
{{
  "selected_policy_slots": ["example_slot"]
}}
""".strip()
        raw = self.provider.complete_text("Return JSON only.", prompt)
        slots = self._parse_selected_slots(raw)
        if not slots:
            return []
        selected = []
        seen = set(slots)
        for item in policies:
            slot = str(item.get("policy_slot", "")).strip().lower()
            if slot and slot in seen:
                selected.append(item)
        return selected

    @staticmethod
    def _parse_selected_slots(raw: str) -> set[str]:
        text = raw.strip()
        if not text:
            return set()
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start == -1 or end == -1 or end <= start:
                return set()
            try:
                parsed = json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return set()
        if not isinstance(parsed, dict):
            return set()
        slots = parsed.get("selected_policy_slots")
        if not isinstance(slots, list):
            return set()
        return {
            str(item).strip().lower()
            for item in slots
            if str(item).strip()
        }
