from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Dict, List

from assistant_app.skills.registry import SkillRegistry


@dataclass
class SkillActionDecision:
    action: str
    raw: str
    skill_id: str = ""
    op: str = ""
    params: Dict[str, Any] = field(default_factory=dict)
    goal: str = ""
    reason: str = ""


def _extract_json_object(text: str) -> Dict | None:
    text = text.strip()
    if not text:
        return None

    candidates = [text]
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        candidates.insert(0, match.group(0))

    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


class SkillPlanner:
    def __init__(self, provider, skill_registry: SkillRegistry, max_skill_steps: int = 6) -> None:
        self.provider = provider
        self.skill_registry = skill_registry
        self.max_skill_steps = max_skill_steps

    def decide(
        self,
        user_message: str,
        recent_history: List[Dict],
        executed_steps: List[Dict],
    ) -> SkillActionDecision:
        if not self.skill_registry.list_skills():
            return SkillActionDecision(action="finish", raw="{}")
        if len(executed_steps) >= self.max_skill_steps:
            return SkillActionDecision(action="finish", raw='{"action":"finish","reason":"max_skill_steps"}')

        history_lines = []
        for item in recent_history[-6:]:
            role = str(item.get("role", "")).strip()
            text = str(item.get("text", "")).strip()
            if role and text:
                history_lines.append(f"{role}: {text}")

        executed_calls = self._format_executed_calls(executed_steps)
        last_skill_state = self._format_last_skill_state(executed_steps)
        prompt = (
            "HISTÓRICO RECENTE\n"
            f"{chr(10).join(history_lines) if history_lines else 'Sem histórico relevante.'}\n\n"
            "MENSAGEM ATUAL DO USUÁRIO\n"
            f"{user_message}\n\n"
            "SKILLS DISPONÍVEIS\n"
            f"{self.skill_registry.format_for_prompt()}\n\n"
            "CHAMADAS DE SKILL JÁ EXECUTADAS NESTE TURNO\n"
            f"{executed_calls}\n\n"
            "ESTADO RESUMIDO DA ÚLTIMA SKILL EXECUTADA\n"
            f"{last_skill_state}"
        )
        instructions = (
            "Você controla o próximo passo do assistant dentro do mesmo turno.\n"
            "Retorne JSON puro, sem markdown.\n"
            'Se precisar executar uma skill agora: {"action":"skill","skill_id":"...","op":"...","params":{...},"goal":"...","reason":"..."}\n'
            'Se já houver informação suficiente e o assistant deve parar de agir: {"action": "finish", "reason": "..."}\n'
            "Regras:\n"
            "- Escolha no máximo uma skill por decisão.\n"
            "- Você pode decidir várias vezes no mesmo turno, após cada saída de skill.\n"
            "- Só escolha skill quando a resposta exigir trabalho externo real antes da resposta final.\n"
            "- Se as ações já executadas neste turno forem suficientes, retorne finish.\n"
            "- A skill pode ser chamada várias vezes no mesmo turno, desde que cada chamada faça a próxima ação útil sobre o que já foi observado.\n"
            "- Se a última saída da skill expôs available_tools, missing_from_current_view, current_view ou content_artifact_summary, use isso para decidir a próxima chamada.\n"
            "- A skill não decide a operação. Você deve escolher op e params explicitamente.\n"
            "- Quando ainda não existir artefato de links e conteúdo neste turno, a primeira operação do browser deve ser search ou navigate.\n"
            "- Use search quando o usuário pedir descoberta geral na web; use navigate quando já houver URL específica.\n"
            "- Use search_artifact, filter_links, list_hosts e get_chunks somente depois que search ou navigate já tiver criado artefato.\n"
            "- Evite repetir exatamente o mesmo goal sem ganho novo de informação.\n"
            "- O campo goal deve ser a tarefa concreta a executar, em português, sem inventar requisitos extras.\n"
            "- Use apenas skill_id existente no catálogo."
        )

        raw = self.provider.complete_text(instructions, prompt).strip()
        parsed = _extract_json_object(raw)
        if not parsed:
            return SkillActionDecision(action="finish", raw=raw)

        action = str(parsed.get("action", "finish")).strip().lower()
        if action != "skill":
            finish_decision = SkillActionDecision(
                action="finish",
                raw=raw,
                reason=str(parsed.get("reason", "")).strip(),
            )
            if executed_steps:
                return self._review_finish(user_message, recent_history, executed_steps, finish_decision)
            return finish_decision

        skill_id = str(parsed.get("skill_id", "")).strip()
        op = str(parsed.get("op", "")).strip()
        params = parsed.get("params") if isinstance(parsed.get("params"), dict) else {}
        goal = str(parsed.get("goal", "")).strip()
        reason = str(parsed.get("reason", "")).strip()
        if not skill_id or not op or not goal:
            return SkillActionDecision(action="finish", raw=raw)
        if self.skill_registry.get(skill_id) is None:
            return SkillActionDecision(action="finish", raw=raw)
        return SkillActionDecision(
            action="skill",
            skill_id=skill_id,
            op=op,
            params=params,
            goal=goal,
            reason=reason,
            raw=raw,
        )

    def _review_finish(
        self,
        user_message: str,
        recent_history: List[Dict],
        executed_steps: List[Dict],
        finish_decision: SkillActionDecision,
    ) -> SkillActionDecision:
        if len(executed_steps) >= self.max_skill_steps:
            return finish_decision

        history_lines = []
        for item in recent_history[-6:]:
            role = str(item.get("role", "")).strip()
            text = str(item.get("text", "")).strip()
            if role and text:
                history_lines.append(f"{role}: {text}")

        executed_calls = self._format_executed_calls(executed_steps)
        last_skill_state = self._format_last_skill_state(executed_steps)
        prompt = (
            "HISTÓRICO RECENTE\n"
            f"{chr(10).join(history_lines) if history_lines else 'Sem histórico relevante.'}\n\n"
            "MENSAGEM ATUAL DO USUÁRIO\n"
            f"{user_message}\n\n"
            "CHAMADAS DE SKILL JÁ EXECUTADAS NESTE TURNO\n"
            f"{executed_calls}\n\n"
            "ESTADO RESUMIDO DA ÚLTIMA SKILL EXECUTADA\n"
            f"{last_skill_state}\n\n"
            "DECISÃO DE ENCERRAR QUE PRECISA SER REVISADA\n"
            f"{json.dumps({'action': finish_decision.action, 'reason': finish_decision.reason}, ensure_ascii=False)}\n\n"
            "SKILLS DISPONÍVEIS\n"
            f"{self.skill_registry.format_for_prompt()}"
        )
        instructions = (
            "Você é o revisor final do encadeamento de skills do mesmo turno.\n"
            "Sua função é verificar se a decisão de finish realmente tem material suficiente para responder exatamente ao que o usuário pediu.\n"
            "Retorne JSON puro, sem markdown.\n"
            'Se a decisão de finish estiver correta: {"verdict":"approve","reason":"..."}\n'
            'Se a decisão de finish estiver errada e ainda faltar uma ação útil: {"verdict":"continue","skill_id":"...","op":"...","params":{...},"goal":"...","reason":"..."}\n'
            "Regras:\n"
            "- Reprove o finish quando a saída atual for apenas sample ou partial e o pedido do usuário exigir lista completa, itens completos, valores completos ou verificação completa.\n"
            "- Reprove o finish quando missing_from_current_view mostrar explicitamente que ainda falta a visão necessária para responder.\n"
            "- Aprove o finish apenas quando a saída já contiver material suficiente para a resposta final sem placeholders.\n"
            "- Se reprovar, proponha exatamente a próxima ação útil, sem repetir uma ação já feita sem ganho novo.\n"
            "- Você deve escolher op e params explicitamente.\n"
            "- Use apenas skill_id existente no catálogo."
        )

        raw = self.provider.complete_text(instructions, prompt).strip()
        parsed = _extract_json_object(raw)
        if not parsed:
            return finish_decision

        verdict = str(parsed.get("verdict", "approve")).strip().lower()
        if verdict != "continue":
            return SkillActionDecision(
                action="finish",
                raw=raw,
                reason=str(parsed.get("reason", "")).strip() or finish_decision.reason,
            )

        skill_id = str(parsed.get("skill_id", "")).strip()
        op = str(parsed.get("op", "")).strip()
        params = parsed.get("params") if isinstance(parsed.get("params"), dict) else {}
        goal = str(parsed.get("goal", "")).strip()
        reason = str(parsed.get("reason", "")).strip()
        if not skill_id or not op or not goal:
            return finish_decision
        if self.skill_registry.get(skill_id) is None:
            return finish_decision
        return SkillActionDecision(
            action="skill",
            skill_id=skill_id,
            op=op,
            params=params,
            goal=goal,
            reason=reason,
            raw=raw,
        )

    def _format_executed_calls(self, executed_steps: List[Dict]) -> str:
        if not executed_steps:
            return "Nenhuma skill executada ainda neste turno."

        lines: List[str] = []
        for index, step in enumerate(executed_steps, start=1):
            skill_id = str(step.get("skill_id", "")).strip() or "desconhecida"
            op = str(step.get("op", "")).strip() or "sem_op"
            params = step.get("params") if isinstance(step.get("params"), dict) else {}
            params_text = json.dumps(params, ensure_ascii=False, sort_keys=True)
            if len(params_text) > 280:
                params_text = params_text[:280].rstrip() + "... [truncated]"
            lines.append(f"{index}. {skill_id}.{op}({params_text})")
        return "\n".join(lines)

    def _format_last_skill_state(self, executed_steps: List[Dict]) -> str:
        if not executed_steps:
            return "Nenhum estado de skill disponível."

        last_step = executed_steps[-1]
        payload = last_step.get("payload") if isinstance(last_step.get("payload"), dict) else {}
        compact = {
            "skill_id": last_step.get("skill_id", ""),
            "op": last_step.get("op", ""),
            "goal": last_step.get("goal", ""),
            "summary": last_step.get("summary", ""),
            "page_state": payload.get("page_state"),
            "current_view": payload.get("current_view"),
            "missing_from_current_view": payload.get("missing_from_current_view"),
            "available_tools": payload.get("available_tools"),
            "content_artifact_summary": payload.get("content_artifact_summary"),
            "filter": payload.get("filter"),
            "query": payload.get("query"),
            "result": self._compact_result(payload.get("result")),
            "error": payload.get("error"),
        }
        return json.dumps(compact, ensure_ascii=False, indent=2)

    def _compact_result(self, result: Any) -> Any:
        if not isinstance(result, dict):
            return result
        compact = dict(result)
        if isinstance(compact.get("results"), list):
            compact["results"] = compact["results"][:3]
        if isinstance(compact.get("links"), list):
            compact["links"] = compact["links"][:5]
        if isinstance(compact.get("matches"), list):
            compact["matches"] = compact["matches"][:5]
        return compact
