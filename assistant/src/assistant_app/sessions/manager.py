from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class SessionInfo:
    session_key: str
    session_id: str
    transcript_path: Path
    history_cursor_at: str


class SessionManager:
    def __init__(self, sqlite_path: Path, transcripts_dir: Path) -> None:
        self.sqlite_path = sqlite_path
        self.transcripts_dir = transcripts_dir

    def get_or_create(self, session_key: str) -> SessionInfo:
        with sqlite3.connect(self.sqlite_path) as conn:
            row = conn.execute(
                "SELECT session_id, updated_at FROM session_state WHERE session_key = ?",
                (session_key,),
            ).fetchone()
            if row:
                session_id = row[0]
                updated_at = row[1]
            else:
                session_id = str(uuid.uuid4())
                updated_at = utc_now()
                conn.execute(
                    "INSERT INTO session_state (session_key, session_id, updated_at) VALUES (?, ?, ?)",
                    (session_key, session_id, updated_at),
                )
                conn.commit()
        transcript_path = self.transcripts_dir / f"{session_id}.jsonl"
        return SessionInfo(session_key=session_key, session_id=session_id, transcript_path=transcript_path, history_cursor_at=updated_at)

    def reset(self, session_key: str) -> SessionInfo:
        session_id = str(uuid.uuid4())
        updated_at = utc_now()
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO session_state (session_key, session_id, updated_at) VALUES (?, ?, ?)",
                (session_key, session_id, updated_at),
            )
            conn.commit()
        transcript_path = self.transcripts_dir / f"{session_id}.jsonl"
        return SessionInfo(session_key=session_key, session_id=session_id, transcript_path=transcript_path, history_cursor_at=updated_at)

    def append_entry(self, session: SessionInfo, entry: Dict) -> None:
        session.transcript_path.parent.mkdir(parents=True, exist_ok=True)
        with open(session.transcript_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                "UPDATE session_state SET updated_at = ? WHERE session_key = ?",
                (utc_now(), session.session_key),
            )
            conn.commit()

    def tail(self, session: SessionInfo, limit: int = 12, since_created_at: str | None = None) -> List[Dict]:
        if not session.transcript_path.exists():
            return []
        with open(session.transcript_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-limit:]
        items = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue
            if since_created_at:
                created_at = str(item.get("created_at", "")).strip()
                if created_at and created_at < since_created_at:
                    continue
            items.append(item)
        return items

    def list_conversations(
        self,
        *,
        limit: int = 10,
        order: str = "recent",
        day: str = "",
    ) -> List[Dict]:
        limit = max(1, min(limit, 50))
        order_sql = "DESC" if order != "oldest" else "ASC"
        with sqlite3.connect(self.sqlite_path) as conn:
            rows = conn.execute(
                f"""
                SELECT session_key, session_id, updated_at
                FROM session_state
                ORDER BY updated_at {order_sql}
                """
            ).fetchall()
        results: List[Dict] = []
        for session_key, session_id, updated_at in rows:
            if day and not str(updated_at).startswith(day):
                continue
            transcript_path = self.transcripts_dir / f"{session_id}.jsonl"
            summary = self._conversation_summary(session_key, session_id, transcript_path, updated_at)
            if not summary:
                continue
            results.append(summary)
            if len(results) >= limit:
                break
        return results

    def search_conversations(
        self,
        *,
        query: str,
        limit: int = 10,
        day: str = "",
    ) -> List[Dict]:
        tokens = self._tokenize(query)
        phrase = " ".join(tokens)
        if not tokens:
            return []
        with sqlite3.connect(self.sqlite_path) as conn:
            rows = conn.execute(
                """
                SELECT session_key, session_id, text, created_at
                FROM transcript_corpus
                ORDER BY created_at DESC
                """
            ).fetchall()
        scored: Dict[str, Dict] = {}
        for session_key, session_id, text, created_at in rows:
            if day and not str(created_at).startswith(day):
                continue
            normalized = self._normalize_text(str(text))
            score = self._score_text_match(phrase, tokens, normalized)
            if score <= 0:
                continue
            current = scored.get(session_id)
            snippet = str(text).strip().replace("\n", " ")
            if len(snippet) > 220:
                snippet = snippet[:220].rstrip() + "... [truncated]"
            if current is None:
                transcript_path = self.transcripts_dir / f"{session_id}.jsonl"
                summary = self._conversation_summary(session_key, session_id, transcript_path, created_at) or {
                    "session_key": session_key,
                    "session_id": session_id,
                    "updated_at": created_at,
                    "message_count": 0,
                    "first_user_message": "",
                    "last_message": "",
                }
                current = {
                    **summary,
                    "score": 0.0,
                    "matched_snippets": [],
                }
                scored[session_id] = current
            current["score"] += score
            current["updated_at"] = max(str(current.get("updated_at", "")), str(created_at))
            snippets = current["matched_snippets"]
            if snippet and snippet not in snippets:
                snippets.append(snippet)
                if len(snippets) > 3:
                    del snippets[3:]
        results = list(scored.values())
        results.sort(key=lambda item: (float(item.get("score", 0.0)), str(item.get("updated_at", ""))), reverse=True)
        return results[: max(1, min(limit, 50))]

    def read_conversation(
        self,
        *,
        session_key: str = "",
        session_id: str = "",
        ordinal: int = 0,
        order: str = "recent",
        day: str = "",
        message_limit: int = 20,
    ) -> Dict:
        target: Dict | None = None
        if session_id:
            if not session_key:
                session_key = self._session_key_for_session_id(session_id)
            transcript_path = self.transcripts_dir / f"{session_id}.jsonl"
            target = self._conversation_summary(session_key, session_id, transcript_path, "")
        elif session_key:
            info = self.get_or_create(session_key)
            target = self._conversation_summary(info.session_key, info.session_id, info.transcript_path, info.history_cursor_at)
        elif ordinal > 0:
            conversations = self.list_conversations(limit=max(ordinal, 20), order=order, day=day)
            if ordinal <= len(conversations):
                target = conversations[ordinal - 1]
        if not target:
            return {}

        transcript_path = self.transcripts_dir / f"{target['session_id']}.jsonl"
        items = self._read_entries(transcript_path)
        messages = []
        for item in items[-max(1, min(message_limit, 80)):]:
            text = str(item.get("text", "")).strip()
            role = str(item.get("role", "")).strip()
            if not role or not text:
                continue
            messages.append(
                {
                    "role": role,
                    "text": text,
                    "turn_id": item.get("turn_id", ""),
                    "created_at": item.get("created_at", ""),
                    "type": item.get("type", ""),
                }
            )
        return {
            **target,
            "messages": messages,
        }

    def _session_key_for_session_id(self, session_id: str) -> str:
        with sqlite3.connect(self.sqlite_path) as conn:
            row = conn.execute(
                "SELECT session_key FROM session_state WHERE session_id = ?",
                (session_id,),
            ).fetchone()
            if row and row[0]:
                return str(row[0])
            row = conn.execute(
                """
                SELECT session_key
                FROM transcript_corpus
                WHERE session_id = ?
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (session_id,),
            ).fetchone()
            return str(row[0]) if row and row[0] else ""

    def _read_entries(self, transcript_path: Path) -> List[Dict]:
        if not transcript_path.exists():
            return []
        items: List[Dict] = []
        with open(transcript_path, "r", encoding="utf-8") as f:
            for raw in f:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    items.append(json.loads(raw))
                except json.JSONDecodeError:
                    continue
        return items

    def _conversation_summary(self, session_key: str, session_id: str, transcript_path: Path, updated_at: str) -> Dict | None:
        items = self._read_entries(transcript_path)
        if not items:
            return None
        messages = [item for item in items if item.get("type") == "message"]
        first_user_message = ""
        last_message = ""
        created_at = ""
        for item in messages:
            if item.get("role") == "user" and not first_user_message:
                first_user_message = str(item.get("text", "")).strip().replace("\n", " ")
            text = str(item.get("text", "")).strip().replace("\n", " ")
            if text:
                last_message = text
                created_at = str(item.get("created_at", "")).strip() or created_at
        if len(first_user_message) > 180:
            first_user_message = first_user_message[:180].rstrip() + "... [truncated]"
        if len(last_message) > 180:
            last_message = last_message[:180].rstrip() + "... [truncated]"
        digest = hashlib.sha1(f"{session_key}:{session_id}".encode("utf-8")).hexdigest()[:8]
        return {
            "conversation_ref": f"conv:{digest}",
            "session_key": session_key,
            "session_id": session_id,
            "updated_at": updated_at or created_at,
            "message_count": len(messages),
            "first_user_message": first_user_message,
            "last_message": last_message,
        }

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

    def _score_text_match(self, phrase: str, tokens: List[str], normalized: str) -> float:
        if not normalized:
            return 0.0
        score = 0.0
        if phrase and phrase in normalized:
            score += 3.0
        for token in tokens:
            if token in normalized:
                score += 1.0
        return score
