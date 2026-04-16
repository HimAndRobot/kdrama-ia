from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from pathlib import Path
import urllib.request
from typing import Dict, Iterable, List, Optional


def _decode_jwt_payload(token: str) -> Dict | None:
    parts = token.split(".")
    if len(parts) < 2:
        return None
    try:
        payload = parts[1].replace("-", "+").replace("_", "/")
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.b64decode(payload).decode("utf-8"))
    except Exception:
        return None


def _parse_chatgpt_account_id(token: str) -> Optional[str]:
    payload = _decode_jwt_payload(token)
    if not payload:
        return None
    nested = payload.get("https://api.openai.com/auth")
    if isinstance(nested, dict) and nested.get("chatgpt_account_id"):
        return str(nested["chatgpt_account_id"])
    return payload.get("https://api.openai.com/auth.chatgpt_account_id") or payload.get("chatgpt_account_id")


@dataclass
class CodexCredentials:
    api_key: str
    account_id: str


class Provider:
    def stream_generate(self, prompt: str, memory_context: Dict, recent_history: List[Dict]) -> Iterable[str]:
        raise NotImplementedError

    def complete_text(self, instructions: str, prompt: str) -> str:
        raise NotImplementedError


def _format_memory_context(memory_context: Dict) -> str:
    profile = memory_context.get("profile") or {}
    recent_memories = memory_context.get("recent_memories") or []

    lines: List[str] = [
        "Perfil consolidado:",
        str(profile.get("profile_text") or "Nenhuma memória consolidada ainda."),
        "",
        f"Memórias recentes desde {profile.get('consolidated_at') or 'o último perfil'}:",
    ]
    if not recent_memories:
        lines.append("- Nenhuma memória recente desde a última consolidação.")
        return "\n".join(lines)

    for item in recent_memories:
        memory_type = item.get("memory_type", "")
        subject = item.get("subject", "")
        value = item.get("value") or {}
        snippet = item.get("snippet") or ""

        if memory_type == "user_identity":
            preferred_name = value.get("preferred_name")
            given_name = value.get("given_name")
            if preferred_name:
                lines.append(f"- Identidade recente: o usuário prefere ser chamado de {preferred_name}")
                continue
            if given_name:
                lines.append(f"- Identidade recente: o nome do usuário é {given_name}")
                continue

        if memory_type == "catalog_seen":
            lines.append(f"- Catálogo recente: o usuário já viu {subject}")
            continue

        if memory_type in ("temporary_preference", "durable_preference"):
            pref = value.get("summary") or value.get("preference") or subject
            label = "preferência temporária" if memory_type == "temporary_preference" else "preferência"
            lines.append(f"- Preferência recente: {label} = {pref}")
            continue

        if snippet:
            lines.append(f"- Nota recente: {snippet}")
        else:
            lines.append(f"- Nota recente: {memory_type} {subject} {json.dumps(value, ensure_ascii=False)}")
    return "\n".join(lines)


def _format_recent_history(recent_history: List[Dict]) -> str:
    if not recent_history:
        return "Nenhum histórico recente."
    lines: List[str] = []
    for item in recent_history:
        role = str(item.get("role", "")).strip() or "unknown"
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        lines.append(f"{role}: {text}")
    return "\n".join(lines) if lines else "Nenhum histórico recente."


class LocalFallbackProvider(Provider):
    def stream_generate(self, prompt: str, memory_context: Dict, recent_history: List[Dict]) -> Iterable[str]:
        lines = []
        if recent_history:
            lines.append("Histórico recente:")
            for item in recent_history[-6:]:
                if item.get("text"):
                    lines.append(f"- {item.get('role')}: {item.get('text')}")
        lines.append("Memória:")
        lines.append(_format_memory_context(memory_context))
        lines.append("")
        lines.append("Resposta local provisória:")
        lines.append(f"Você disse: {prompt}")
        yield "\n".join(lines).strip()

    def complete_text(self, instructions: str, prompt: str) -> str:
        return "[]"


class OpenAIProvider(Provider):
    def __init__(self, api_key: str, model: str) -> None:
        self.api_key = api_key
        self.model = model

    def stream_generate(self, prompt: str, memory_context: Dict, recent_history: List[Dict]) -> Iterable[str]:
        system = (
            "You are a personal assistant. Respond in Brazilian Portuguese. "
            "You will receive recent conversation history, memory context, and the current user message. "
            "The current user message is always the primary thing to answer. "
            "Memory context has two layers: a consolidated profile and recent memory updates since that profile. Recent memory updates override or refine the consolidated profile when they conflict. "
            "Do not imitate historical wording. "
            "Do not repeat the user's name in every answer; use it only when natural and helpful. "
            "Respond in Brazilian Portuguese."
        )
        memory_text = _format_memory_context(memory_context)
        history_text = _format_recent_history(recent_history)
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": (
                        "RECENT CONVERSATION HISTORY\n"
                        f"{history_text}\n\n"
                        "MEMORY CONTEXT\n"
                        f"{memory_text}\n\n"
                        "CURRENT USER MESSAGE\n"
                        f"{prompt}"
                    ),
                },
            ],
        }
        data = self._post_json("https://api.openai.com/v1/responses", payload)
        yield self._extract_non_stream_text(data)

    def complete_text(self, instructions: str, prompt: str) -> str:
        payload = {
            "model": self.model,
            "input": [
                {"role": "system", "content": instructions},
                {"role": "user", "content": prompt},
            ],
        }
        data = self._post_json("https://api.openai.com/v1/responses", payload)
        return self._extract_non_stream_text(data)

    def _post_json(self, url: str, payload: Dict) -> Dict:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))

    @staticmethod
    def _extract_non_stream_text(data: Dict) -> str:
        for item in data.get("output", []):
            if item.get("type") == "message":
                texts = [part.get("text", "") for part in item.get("content", []) if part.get("type") in ("output_text", "text")]
                if texts:
                    return "".join(texts).strip()
        return ""


class CodexProvider(Provider):
    def __init__(self, auth_path: Path, base_url: str, model: str = "gpt-5.4") -> None:
        self.auth_path = auth_path
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.credentials = self._load_credentials()

    def _load_credentials(self) -> CodexCredentials:
        env_api_key = ""
        env_account_id = ""
        try:
            import os

            env_api_key = os.getenv("CODEX_API_KEY", "").strip()
            env_account_id = (os.getenv("CHATGPT_ACCOUNT_ID") or os.getenv("CODEX_ACCOUNT_ID") or "").strip()
        except Exception:
            pass
        if env_api_key:
            return CodexCredentials(
                api_key=env_api_key,
                account_id=env_account_id or _parse_chatgpt_account_id(env_api_key) or "",
            )

        auth = {}
        if self.auth_path.exists():
            auth = json.loads(self.auth_path.read_text(encoding="utf-8"))
        tokens = auth.get("tokens") if isinstance(auth.get("tokens"), dict) else {}
        api_key = (
            auth.get("openai_api_key")
            or auth.get("OPENAI_API_KEY")
            or tokens.get("access_token")
            or tokens.get("accessToken")
            or ""
        )
        account_id = (
            auth.get("account_id")
            or auth.get("accountId")
            or tokens.get("account_id")
            or tokens.get("accountId")
            or _parse_chatgpt_account_id(str(api_key))
            or ""
        )
        api_key = str(api_key).strip()
        account_id = str(account_id).strip()
        if not api_key or not account_id:
            raise RuntimeError(f"Codex auth incompleto em {self.auth_path}")
        return CodexCredentials(api_key=api_key, account_id=account_id)

    def stream_generate(self, prompt: str, memory_context: Dict, recent_history: List[Dict]) -> Iterable[str]:
        instructions = (
            "You are a personal assistant. Respond in Brazilian Portuguese.\n"
            "You will receive exactly three blocks:\n"
            "1. RECENT CONVERSATION HISTORY\n"
            "2. MEMORY CONTEXT\n"
            "3. CURRENT USER MESSAGE\n\n"
            "Contract:\n"
            "- The CURRENT USER MESSAGE is always the main thing to answer.\n"
            "- RECENT CONVERSATION HISTORY is the primary conversational context and should be used to preserve continuity.\n"
            "- MEMORY CONTEXT has two layers: consolidated profile and recent memory updates since that profile.\n"
            "- Recent memory updates are newer than the consolidated profile. If they conflict, the recent memory updates refine or override the consolidated profile.\n"
            "- Use memory only when it materially helps answer the current message.\n"
            "- Do not imitate historical wording.\n"
            "- Do not repeat the user's name in every answer; use it only when natural and helpful.\n"
            "- If memory contains the user's name and the user asks their name, answer with it directly.\n"
            "- If memory contains a fact needed to answer, use it directly instead of claiming not to know.\n"
        )
        memory_text = _format_memory_context(memory_context)
        history_text = _format_recent_history(recent_history)
        body = self._build_body(
            instructions=instructions,
            prompt=(
                "RECENT CONVERSATION HISTORY\n"
                f"{history_text}\n\n"
                "MEMORY CONTEXT\n"
                f"{memory_text}\n\n"
                "CURRENT USER MESSAGE\n"
                f"{prompt}"
            ),
        )
        yield from self._stream_response_text(body)

    def complete_text(self, instructions: str, prompt: str) -> str:
        body = self._build_body(instructions=instructions, prompt=prompt)
        return "".join(self._stream_response_text(body)).strip()

    def _build_body(self, *, instructions: str, prompt: str) -> Dict:
        return {
            "model": self.model,
            "instructions": instructions,
            "input": [
                {
                    "type": "message",
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        }
                    ],
                }
            ],
            "store": False,
            "stream": True,
        }

    def _stream_response_text(self, body: Dict) -> Iterable[str]:
        req = urllib.request.Request(
            f"{self.base_url}/responses",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.credentials.api_key}",
                "chatgpt-account-id": self.credentials.account_id,
                "originator": "assistant-app",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            buffer = ""
            emitted_any_text = False
            for raw in resp:
                buffer += raw.decode("utf-8")
                while "\n\n" in buffer:
                    chunk, buffer = buffer.split("\n\n", 1)
                    event_name = None
                    data_payload = None
                    for line in chunk.splitlines():
                        if line.startswith("event: "):
                            event_name = line[7:].strip()
                        elif line.startswith("data: "):
                            data_payload = line[6:]
                    if not event_name or not data_payload or data_payload == "[DONE]":
                        continue
                    try:
                        payload = json.loads(data_payload)
                    except json.JSONDecodeError:
                        continue
                    if event_name == "response.output_text.delta":
                        delta = payload.get("delta", "")
                        if delta:
                            emitted_any_text = True
                            yield delta
                    elif event_name in ("response.completed", "response.incomplete"):
                        response = payload.get("response") or {}
                        output = response.get("output") or []
                        fallback_parts: List[str] = []
                        for item in output:
                            if item.get("type") != "message":
                                continue
                            for part in item.get("content", []):
                                text = part.get("text", "")
                                if text:
                                    fallback_parts.append(text)
                        if fallback_parts and not emitted_any_text:
                            yield "".join(fallback_parts)
                        return
