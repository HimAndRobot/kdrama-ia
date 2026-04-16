from __future__ import annotations

import json
from typing import Any, Dict, List

from assistant_app.sessions.manager import SessionManager
from assistant_app.skills.registry import SkillExecutionContext, SkillRunResult


class SkillHistoryTool:
    def __init__(self, session_manager: SessionManager) -> None:
        self.session_manager = session_manager

    def describe_operations(self) -> List[Dict[str, Any]]:
        return [
            {
                "op": "last_skill_calls",
                "description": "Consulta as últimas skill calls da sessão atual, com skill, operação, parâmetros e resumo curto do que aconteceu.",
                "params": '{"limit":5}',
                "precondition": "Nenhuma. Use quando precisar recuperar o que já foi chamado antes ou revisar uma sequência de ações.",
            }
        ]

    def __call__(self, context: SkillExecutionContext) -> SkillRunResult:
        metadata = context.metadata if isinstance(context.metadata, dict) else {}
        params = metadata.get("params") if isinstance(metadata.get("params"), dict) else {}
        op = str(metadata.get("op", "")).strip() or "last_skill_calls"
        if op != "last_skill_calls":
            raise RuntimeError(f"Operação de skill não suportada: {op}")

        limit = max(1, min(int(params.get("limit", 5) or 5), 20))
        session = self.session_manager.get_or_create(context.session_key)
        items = self.session_manager.tail(session, limit=200)
        calls = [item for item in items if item.get("type") == "skill_call"]
        recent_calls = calls[-limit:]

        result_calls = []
        for item in recent_calls:
            result_calls.append(
                {
                    "turn_id": item.get("turn_id", ""),
                    "skill_id": item.get("skill_id", ""),
                    "op": item.get("op", ""),
                    "params": item.get("params", {}),
                    "goal": item.get("goal", ""),
                    "status": item.get("status", "ok"),
                    "summary": item.get("summary", ""),
                    "created_at": item.get("created_at", ""),
                }
            )

        payload = {
            "requested_goal": context.goal,
            "resolved_operation": "last_skill_calls",
            "result": {
                "calls": result_calls,
                "count": len(result_calls),
            },
            "current_view": {
                "kind": "recent_skill_calls",
                "coverage": "complete",
                "returned_count": len(result_calls),
                "total_count": len(result_calls),
            },
            "available_tools": [],
            "missing_from_current_view": [],
        }

        summary = self._build_summary(result_calls)
        return SkillRunResult(
            skill_id="skill-history",
            goal=context.goal,
            summary=summary,
            payload=payload,
        )

    def _build_summary(self, calls: List[Dict[str, Any]]) -> str:
        if not calls:
            return "Skill skill-history executada: nenhuma skill call recente encontrada."

        lines = ["Skill skill-history executada: últimas skill calls da sessão"]
        for index, call in enumerate(calls, start=1):
            params_text = json.dumps(call.get("params", {}), ensure_ascii=False, sort_keys=True)
            if len(params_text) > 220:
                params_text = params_text[:220].rstrip() + "... [truncated]"
            lines.append(
                f"{index}. {call.get('skill_id', 'desconhecida')}.{call.get('op', 'sem_op')}({params_text}) "
                f"[{call.get('status', 'ok')}]"
            )
        return "\n".join(lines)
