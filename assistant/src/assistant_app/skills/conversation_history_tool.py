from __future__ import annotations

import json
from typing import Any, Dict, List

from assistant_app.sessions.manager import SessionManager
from assistant_app.skills.registry import SkillExecutionContext, SkillRunResult


class ConversationHistoryTool:
    def __init__(self, session_manager: SessionManager, provider=None) -> None:
        self.session_manager = session_manager
        self.provider = provider

    def describe_operations(self) -> List[Dict[str, Any]]:
        return [
            {
                "op": "list_conversations",
                "description": "Lista conversas anteriores por ordem cronológica, com filtro opcional por dia.",
                "params": '{"limit":5,"order":"recent","day":"2026-04-16"}',
                "precondition": "Nenhuma. Use quando precisar lembrar ou localizar uma conversa anterior sem saber o conteúdo exato.",
            },
            {
                "op": "search_conversations",
                "description": "Busca conversas anteriores por proximidade textual/tags livres, com filtro opcional por dia.",
                "params": '{"query":"reset drive weifansub","limit":5,"day":"2026-04-16"}',
                "precondition": "Nenhuma. Use quando o usuário citar assunto, termos ou tags soltas de uma conversa passada.",
            },
            {
                "op": "read_conversation",
                "description": "Abre uma conversa anterior específica por ordem, session_key ou session_id e devolve um recorte das mensagens.",
                "params": '{"ordinal":1,"order":"recent","day":"2026-04-16","message_limit":12}',
                "precondition": "Exige session_id, session_key ou ordinal válido dentro da lista filtrada.",
            },
            {
                "op": "summarize_conversation",
                "description": "Resume uma conversa anterior com foco em uma frase/tema específico, usando session_id/session_key/ordinal ou a melhor conversa encontrada pela query.",
                "params": '{"query":"doramore episódio 1","ordinal":1,"order":"recent","message_limit":16}',
                "precondition": "Exige query ou um alvo de conversa válido para resumir.",
            },
        ]

    def __call__(self, context: SkillExecutionContext) -> SkillRunResult:
        metadata = context.metadata if isinstance(context.metadata, dict) else {}
        params = metadata.get("params") if isinstance(metadata.get("params"), dict) else {}
        op = str(metadata.get("op", "")).strip() or "list_conversations"
        if op == "list_conversations":
            result = self._list_conversations(params)
        elif op == "search_conversations":
            result = self._search_conversations(params)
        elif op == "read_conversation":
            result = self._read_conversation(params)
        elif op == "summarize_conversation":
            result = self._summarize_conversation(params)
        else:
            raise RuntimeError(f"Operação de skill não suportada: {op}")

        payload = {
            "requested_goal": context.goal,
            "resolved_operation": op,
            **result,
        }
        return SkillRunResult(
            skill_id="conversation-history",
            goal=context.goal,
            summary=self._build_summary(op, payload),
            payload=payload,
        )

    def _list_conversations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        limit = max(1, min(int(params.get("limit", 5) or 5), 20))
        order = str(params.get("order", "recent") or "recent").strip().lower()
        day = str(params.get("day", "") or "").strip()
        items = self.session_manager.list_conversations(limit=limit, order=order, day=day)
        return {
            "result": {"conversations": items, "count": len(items)},
            "current_view": {
                "kind": "conversation_list",
                "coverage": "complete",
                "order": order,
                "day": day,
                "returned_count": len(items),
                "total_count": len(items),
            },
            "available_tools": [],
            "missing_from_current_view": [],
        }

    def _search_conversations(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = str(params.get("query", "") or "").strip()
        if not query:
            raise RuntimeError("search_conversations exige query.")
        limit = max(1, min(int(params.get("limit", 5) or 5), 20))
        day = str(params.get("day", "") or "").strip()
        items = self.session_manager.search_conversations(query=query, limit=limit, day=day)
        return {
            "result": {"conversations": items, "count": len(items), "query": query},
            "current_view": {
                "kind": "conversation_search_results",
                "coverage": "complete",
                "query": query,
                "day": day,
                "returned_count": len(items),
                "total_count": len(items),
            },
            "available_tools": [],
            "missing_from_current_view": [],
        }

    def _read_conversation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        session_key = str(params.get("session_key", "") or "").strip()
        session_id = str(params.get("session_id", "") or "").strip()
        ordinal = int(params.get("ordinal", 0) or 0)
        order = str(params.get("order", "recent") or "recent").strip().lower()
        day = str(params.get("day", "") or "").strip()
        message_limit = max(1, min(int(params.get("message_limit", 12) or 12), 40))
        item = self.session_manager.read_conversation(
            session_key=session_key,
            session_id=session_id,
            ordinal=ordinal,
            order=order,
            day=day,
            message_limit=message_limit,
        )
        if not item:
            raise RuntimeError("Conversa não encontrada para os parâmetros fornecidos.")
        return {
            "result": {"conversation": item},
            "current_view": {
                "kind": "conversation_messages",
                "coverage": "complete",
                "session_key": item.get("session_key", ""),
                "session_id": item.get("session_id", ""),
                "returned_count": len(item.get("messages") or []),
                "total_count": len(item.get("messages") or []),
            },
            "available_tools": [],
            "missing_from_current_view": [],
        }

    def _summarize_conversation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        query = str(params.get("query", "") or "").strip()
        session_key = str(params.get("session_key", "") or "").strip()
        session_id = str(params.get("session_id", "") or "").strip()
        ordinal = int(params.get("ordinal", 0) or 0)
        order = str(params.get("order", "recent") or "recent").strip().lower()
        day = str(params.get("day", "") or "").strip()
        message_limit = max(1, min(int(params.get("message_limit", 16) or 16), 50))

        conversation = self.session_manager.read_conversation(
            session_key=session_key,
            session_id=session_id,
            ordinal=ordinal,
            order=order,
            day=day,
            message_limit=message_limit,
        )
        if not conversation:
            if not query:
                raise RuntimeError("summarize_conversation exige query ou um alvo de conversa.")
            matches = self.session_manager.search_conversations(query=query, limit=1, day=day)
            if not matches:
                raise RuntimeError("Nenhuma conversa encontrada para resumir.")
            conversation = self.session_manager.read_conversation(
                session_id=str(matches[0].get("session_id", "")),
                message_limit=message_limit,
            )
        if not conversation:
            raise RuntimeError("Conversa não encontrada para resumir.")

        summary = self._focus_summary(conversation, query)
        return {
            "result": {
                "conversation": {
                    "conversation_ref": conversation.get("conversation_ref", ""),
                    "session_key": conversation.get("session_key", ""),
                    "session_id": conversation.get("session_id", ""),
                    "updated_at": conversation.get("updated_at", ""),
                    "first_user_message": conversation.get("first_user_message", ""),
                    "last_message": conversation.get("last_message", ""),
                    "message_count": conversation.get("message_count", 0),
                },
                "query": query,
                "summary_text": summary["summary_text"],
                "matched_messages": summary["matched_messages"],
            },
            "current_view": {
                "kind": "conversation_summary",
                "coverage": "complete",
                "session_key": conversation.get("session_key", ""),
                "session_id": conversation.get("session_id", ""),
                "returned_count": len(summary["matched_messages"]),
                "total_count": len(summary["matched_messages"]),
            },
            "available_tools": [],
            "missing_from_current_view": [],
        }

    def _focus_summary(self, conversation: Dict[str, Any], query: str) -> Dict[str, Any]:
        messages = conversation.get("messages") or []
        tokens = self._tokenize(query)
        matched_messages = []
        for item in messages:
            text = str(item.get("text", "") or "").replace("\n", " ").strip()
            if not text:
                continue
            normalized = self._normalize_text(text)
            score = self._score_text_match(tokens, normalized)
            if not tokens:
                score = 1.0
            if score <= 0:
                continue
            snippet = text
            if len(snippet) > 220:
                snippet = snippet[:220].rstrip() + "... [truncated]"
            matched_messages.append(
                {
                    "role": item.get("role", ""),
                    "text": snippet,
                    "created_at": item.get("created_at", ""),
                    "score": score,
                }
            )
        matched_messages.sort(key=lambda item: float(item.get("score", 0.0)), reverse=True)
        matched_messages = matched_messages[:6]

        lines = [
            f"Conversa {conversation.get('conversation_ref','')} [session_key={conversation.get('session_key','')}]",
        ]
        if query:
            lines.append(f"Foco: {query}")
        first_user = str(conversation.get("first_user_message", "") or "").strip()
        if first_user:
            lines.append(f"Início: {first_user}")
        last_message = str(conversation.get("last_message", "") or "").strip()
        if last_message:
            lines.append(f"Fim mais recente: {last_message}")
        if matched_messages:
            lines.append("Trechos relevantes:")
            for item in matched_messages:
                lines.append(f"- {item.get('role','')}: {item.get('text','')}")
        summary_text = "\n".join(lines)
        ai_summary = self._ai_focus_summary(conversation, query, matched_messages)
        if ai_summary:
            summary_text = ai_summary
        return {"summary_text": summary_text, "matched_messages": matched_messages}

    def _ai_focus_summary(self, conversation: Dict[str, Any], query: str, matched_messages: List[Dict[str, Any]]) -> str:
        if self.provider is None:
            return ""
        selected_messages = matched_messages
        if not selected_messages:
            selected_messages = []
            for item in (conversation.get("messages") or [])[-10:]:
                text = str(item.get("text", "") or "").replace("\n", " ").strip()
                if not text:
                    continue
                if len(text) > 220:
                    text = text[:220].rstrip() + "... [truncated]"
                selected_messages.append(
                    {
                        "role": item.get("role", ""),
                        "text": text,
                        "created_at": item.get("created_at", ""),
                        "score": 0.0,
                    }
                )
        prompt = json.dumps(
            {
                "conversation": {
                    "conversation_ref": conversation.get("conversation_ref", ""),
                    "session_key": conversation.get("session_key", ""),
                    "updated_at": conversation.get("updated_at", ""),
                    "first_user_message": conversation.get("first_user_message", ""),
                    "last_message": conversation.get("last_message", ""),
                },
                "focus_query": query,
                "matched_messages": selected_messages[:10],
            },
            ensure_ascii=False,
            indent=2,
        )
        instructions = (
            "Resuma a conversa de forma objetiva em português, com foco no tema pedido.\n"
            "Retorne texto puro.\n"
            "Diga o assunto principal, o que foi descoberto/decidido e qualquer limitação ou resultado final importante.\n"
            "Se houver query de foco, priorize esse tema.\n"
            "Não invente fatos fora das mensagens fornecidas.\n"
            "Seja curto."
        )
        try:
            return self.provider.complete_text(instructions, prompt).strip()
        except Exception:
            return ""

    def _normalize_text(self, value: str) -> str:
        return " ".join(value.lower().split())

    def _tokenize(self, value: str) -> List[str]:
        cleaned = self._normalize_text(value)
        tokens = []
        for token in cleaned.replace("?", " ").replace("!", " ").replace(",", " ").replace(".", " ").split():
            token = token.strip()
            if len(token) >= 3:
                tokens.append(token)
        return tokens

    def _score_text_match(self, tokens: List[str], normalized: str) -> float:
        if not normalized:
            return 0.0
        score = 0.0
        for token in tokens:
            if token in normalized:
                score += 1.0
        return score

    def _build_summary(self, op: str, payload: Dict[str, Any]) -> str:
        result = payload.get("result") or {}
        if op in {"list_conversations", "search_conversations"}:
            conversations = result.get("conversations") or []
            if not conversations:
                return f"Skill conversation-history executada: nenhuma conversa encontrada em {op}."
            lines = [f"Skill conversation-history executada: {op}"]
            for index, item in enumerate(conversations, start=1):
                lines.append(
                    f"{index}. {item.get('conversation_ref','')} "
                    f"[session_key={item.get('session_key','')}] "
                    f"[updated_at={item.get('updated_at','')}] "
                    f"{item.get('first_user_message','')}"
                )
            return "\n".join(lines)

        if op == "summarize_conversation":
            conversation = result.get("conversation") or {}
            return (
                "Skill conversation-history executada: summarize_conversation\n"
                f"Conversa: {conversation.get('conversation_ref','')} [session_key={conversation.get('session_key','')}]\n"
                f"{result.get('summary_text','')}"
            ).strip()

        conversation = result.get("conversation") or {}
        messages = conversation.get("messages") or []
        lines = [
            "Skill conversation-history executada: read_conversation",
            f"Conversa: {conversation.get('conversation_ref','')} [session_key={conversation.get('session_key','')}]",
            f"Mensagens retornadas: {len(messages)}",
        ]
        for index, item in enumerate(messages[:8], start=1):
            role = item.get("role", "")
            text = str(item.get("text", "")).replace("\n", " ")
            if len(text) > 180:
                text = text[:180].rstrip() + "... [truncated]"
            lines.append(f"{index}. {role}: {text}")
        return "\n".join(lines)
