from __future__ import annotations

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
