from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from assistant_app.contracts import MemoryFact


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


def tokenize(value: str) -> List[str]:
    tokens = []
    for token in normalize_text(value).replace("?", " ").replace("!", " ").replace(",", " ").replace(".", " ").split():
        token = token.strip()
        if len(token) >= 3:
            tokens.append(token)
    return tokens


class MemoryStore:
    def __init__(self, sqlite_path: Path) -> None:
        self.sqlite_path = sqlite_path

    def get_context_pack(self, profile_key: str = "main") -> Dict:
        profile = self._get_or_create_profile(profile_key)
        recent_memories = self._list_memories_updated_after(profile["consolidated_at"])
        return {
            "profile": profile,
            "recent_memories": recent_memories,
        }

    def index_transcript_entry(
        self,
        *,
        session_key: str,
        session_id: str,
        turn_id: str,
        role: str,
        text: str,
        source_path: str,
        created_at: str,
    ) -> None:
        entry_key = f"{session_id}:{turn_id}:{role}"
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO transcript_corpus
                (entry_key, session_key, session_id, turn_id, role, text, source_path, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (entry_key, session_key, session_id, turn_id, role, text, source_path, created_at),
            )
            conn.commit()

    def add_candidate_facts(self, facts: List[MemoryFact]) -> None:
        if not facts:
            return
        with sqlite3.connect(self.sqlite_path) as conn:
            now = utc_now()
            for fact in facts:
                self._drop_conflicting_identity_facts(conn, fact)
                if fact.operation == "replace":
                    self._supersede_memory_subject(conn, fact.memory_type, fact.subject, now)
                dedupe_key = self._fact_dedupe_key(fact)
                existing = conn.execute(
                    """
                    SELECT id, confidence, temporal_weight
                    FROM memory_candidates
                    WHERE dedupe_key = ?
                    """,
                    (dedupe_key,),
                ).fetchone()
                if existing:
                    conn.execute(
                        """
                        UPDATE memory_candidates
                        SET value_json = ?, confidence = ?, temporal_weight = ?, status = 'active',
                            source = ?, expires_at = ?, updated_at = ?
                        WHERE dedupe_key = ?
                        """,
                        (
                            json.dumps(fact.value, ensure_ascii=False),
                            max(existing[1], fact.confidence),
                            max(existing[2], fact.temporal_weight),
                            fact.source,
                            fact.expires_at,
                            now,
                            dedupe_key,
                        ),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO memory_candidates
                        (dedupe_key, memory_type, subject, value_json, confidence, temporal_weight, status, source, expires_at, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, 'active', ?, ?, ?, ?)
                        """,
                        (
                            dedupe_key,
                            fact.memory_type,
                            fact.subject,
                            json.dumps(fact.value, ensure_ascii=False),
                            fact.confidence,
                            fact.temporal_weight,
                            fact.source,
                            fact.expires_at,
                            now,
                            now,
                        ),
                    )
            conn.commit()

    def apply_memory_operations(self, operations: List[Dict]) -> None:
        if not operations:
            return
        now = utc_now()
        with sqlite3.connect(self.sqlite_path) as conn:
            for operation in operations:
                if operation.get("operation") != "supersede":
                    continue
                item_key = str(operation.get("item_key", "")).strip()
                if item_key.startswith("candidate:"):
                    dedupe_key = item_key.removeprefix("candidate:")
                    conn.execute(
                        """
                        UPDATE memory_candidates
                        SET status = 'superseded', updated_at = ?
                        WHERE dedupe_key = ? AND status = 'active'
                        """,
                        (now, dedupe_key),
                    )
                    conn.execute("DELETE FROM short_term_recall WHERE item_key = ?", (item_key,))
                    continue
                if item_key.startswith("durable:"):
                    try:
                        memory_id = int(item_key.removeprefix("durable:"))
                    except ValueError:
                        continue
                    conn.execute(
                        """
                        UPDATE memory_items
                        SET status = 'superseded', updated_at = ?
                        WHERE id = ? AND status = 'active'
                        """,
                        (now, memory_id),
                    )
                    conn.execute("DELETE FROM short_term_recall WHERE item_key = ?", (item_key,))
            conn.commit()

    def search(self, query: str, limit: int = 8, exclude_turn_id: Optional[str] = None) -> List[Dict]:
        tokens = tokenize(query)
        phrase = normalize_text(query)
        now = datetime.now(timezone.utc)
        results: List[Dict] = []
        with sqlite3.connect(self.sqlite_path) as conn:
            durable_rows = conn.execute(
                """
                SELECT id, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at
                FROM memory_items
                WHERE status = 'active'
                ORDER BY updated_at DESC
                """
            ).fetchall()
            candidate_rows = conn.execute(
                """
                SELECT dedupe_key, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at
                FROM memory_candidates
                WHERE status = 'active'
                ORDER BY updated_at DESC
                """
            ).fetchall()
            transcript_rows = []

        for row in durable_rows:
            memory_id, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at = row
            if self._is_expired(expires_at, now):
                continue
            value = json.loads(value_json)
            searchable = self._build_searchable_text(subject, value)
            score = self._score_match(phrase, tokens, searchable) + confidence + temporal_weight + 0.5
            if score <= 0:
                continue
            results.append(
                {
                    "kind": "durable",
                    "item_key": f"durable:{memory_id}",
                    "source_ref": "memory_items",
                    "memory_type": memory_type,
                    "subject": subject,
                    "value": value,
                    "snippet": value.get("summary") or subject,
                    "score": score,
                }
            )

        for row in candidate_rows:
            dedupe_key, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at = row
            if self._is_expired(expires_at, now):
                continue
            value = json.loads(value_json)
            searchable = self._build_searchable_text(subject, value)
            score = self._score_match(phrase, tokens, searchable) + confidence + temporal_weight
            if score <= 0:
                continue
            results.append(
                {
                    "kind": "candidate",
                    "item_key": f"candidate:{dedupe_key}",
                    "source_ref": "memory_candidates",
                    "memory_type": memory_type,
                    "subject": subject,
                    "value": value,
                    "snippet": value.get("summary") or subject,
                    "score": score,
                }
            )

        results.sort(key=lambda item: item["score"], reverse=True)
        deduped: List[Dict] = []
        seen = set()
        for item in results:
            key = item["item_key"]
            if key in seen:
                continue
            seen.add(key)
            deduped.append(item)
            if len(deduped) >= limit:
                break
        return deduped

    def _get_or_create_profile(self, profile_key: str) -> Dict:
        with sqlite3.connect(self.sqlite_path) as conn:
            row = conn.execute(
                """
                SELECT profile_text, consolidated_at, updated_at
                FROM memory_profile
                WHERE profile_key = ?
                """,
                (profile_key,),
            ).fetchone()
            if row:
                profile_text, consolidated_at, updated_at = row
                return {
                    "profile_key": profile_key,
                    "profile_text": profile_text,
                    "consolidated_at": consolidated_at,
                    "updated_at": updated_at,
                }

            now = utc_now()
            entries = self._list_all_active_memory_entries(conn)
            profile_text = self._format_profile_text(entries)
            conn.execute(
                """
                INSERT INTO memory_profile (profile_key, profile_text, consolidated_at, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (profile_key, profile_text, now, now, now),
            )
            conn.commit()
            return {
                "profile_key": profile_key,
                "profile_text": profile_text,
                "consolidated_at": now,
                "updated_at": now,
            }

    def rebuild_profile(self, profile_key: str = "main") -> Dict:
        now = utc_now()
        with sqlite3.connect(self.sqlite_path) as conn:
            entries = self._list_all_active_memory_entries(conn)
            profile_text = self._format_profile_text(entries)
            conn.execute(
                """
                INSERT INTO memory_profile (profile_key, profile_text, consolidated_at, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(profile_key) DO UPDATE SET
                    profile_text = excluded.profile_text,
                    consolidated_at = excluded.consolidated_at,
                    updated_at = excluded.updated_at
                """,
                (profile_key, profile_text, now, now, now),
            )
            conn.commit()
        return {
            "profile_key": profile_key,
            "profile_text": profile_text,
            "consolidated_at": now,
            "updated_at": now,
        }

    def list_profile_source_entries(self) -> List[Dict]:
        with sqlite3.connect(self.sqlite_path) as conn:
            return self._list_all_active_memory_entries(conn)

    def set_profile_text(self, profile_text: str, profile_key: str = "main") -> Dict:
        now = utc_now()
        text = profile_text.strip() or "Nenhuma memória consolidada ainda."
        with sqlite3.connect(self.sqlite_path) as conn:
            conn.execute(
                """
                INSERT INTO memory_profile (profile_key, profile_text, consolidated_at, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(profile_key) DO UPDATE SET
                    profile_text = excluded.profile_text,
                    consolidated_at = excluded.consolidated_at,
                    updated_at = excluded.updated_at
                """,
                (profile_key, text, now, now, now),
            )
            conn.commit()
        return {
            "profile_key": profile_key,
            "profile_text": text,
            "consolidated_at": now,
            "updated_at": now,
        }

    def _list_memories_updated_after(self, consolidated_at: str) -> List[Dict]:
        now = datetime.now(timezone.utc)
        with sqlite3.connect(self.sqlite_path) as conn:
            durable_rows = conn.execute(
                """
                SELECT id, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at
                FROM memory_items
                WHERE status = 'active' AND updated_at > ?
                ORDER BY updated_at ASC
                """,
                (consolidated_at,),
            ).fetchall()
            candidate_rows = conn.execute(
                """
                SELECT dedupe_key, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at
                FROM memory_candidates
                WHERE status = 'active' AND updated_at > ?
                ORDER BY updated_at ASC
                """,
                (consolidated_at,),
            ).fetchall()

        items: List[Dict] = []
        seen = set()
        for row in durable_rows:
            memory_id, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at = row
            if self._is_expired(expires_at, now):
                continue
            value = json.loads(value_json)
            key = (memory_type, subject)
            seen.add(key)
            items.append(
                {
                    "kind": "durable",
                    "item_key": f"durable:{memory_id}",
                    "source_ref": "memory_items",
                    "memory_type": memory_type,
                    "subject": subject,
                    "value": value,
                    "snippet": value.get("summary") or subject,
                    "updated_at": updated_at,
                }
            )
        for row in candidate_rows:
            dedupe_key, memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at = row
            if self._is_expired(expires_at, now):
                continue
            value = json.loads(value_json)
            key = (memory_type, subject)
            if key in seen:
                items = [item for item in items if (item["memory_type"], item["subject"]) != key]
            seen.add(key)
            items.append(
                {
                    "kind": "candidate",
                    "item_key": f"candidate:{dedupe_key}",
                    "source_ref": "memory_candidates",
                    "memory_type": memory_type,
                    "subject": subject,
                    "value": value,
                    "snippet": value.get("summary") or subject,
                    "updated_at": updated_at,
                }
            )
        items.sort(key=lambda item: item["updated_at"])
        return items

    def _list_all_active_memory_entries(self, conn: sqlite3.Connection) -> List[Dict]:
        now = datetime.now(timezone.utc)
        durable_rows = conn.execute(
            """
            SELECT id, memory_type, subject, value_json, updated_at, expires_at
            FROM memory_items
            WHERE status = 'active'
            ORDER BY updated_at ASC
            """
        ).fetchall()
        candidate_rows = conn.execute(
            """
            SELECT dedupe_key, memory_type, subject, value_json, updated_at, expires_at
            FROM memory_candidates
            WHERE status = 'active'
            ORDER BY updated_at ASC
            """
        ).fetchall()
        by_subject: Dict[tuple, Dict] = {}
        for memory_id, memory_type, subject, value_json, updated_at, expires_at in durable_rows:
            if self._is_expired(expires_at, now):
                continue
            by_subject[(memory_type, subject)] = {
                "kind": "durable",
                "item_key": f"durable:{memory_id}",
                "source_ref": "memory_items",
                "memory_type": memory_type,
                "subject": subject,
                "value": json.loads(value_json),
                "updated_at": updated_at,
            }
        for dedupe_key, memory_type, subject, value_json, updated_at, expires_at in candidate_rows:
            if self._is_expired(expires_at, now):
                continue
            by_subject[(memory_type, subject)] = {
                "kind": "candidate",
                "item_key": f"candidate:{dedupe_key}",
                "source_ref": "memory_candidates",
                "memory_type": memory_type,
                "subject": subject,
                "value": json.loads(value_json),
                "updated_at": updated_at,
            }
        return sorted(by_subject.values(), key=lambda item: item["updated_at"])

    def _format_profile_text(self, entries: List[Dict]) -> str:
        if not entries:
            return "Nenhuma memória consolidada ainda."
        lines = []
        for item in entries:
            lines.append(f"- {self._memory_entry_to_text(item)}")
        return "\n".join(lines)

    @staticmethod
    def _memory_entry_to_text(item: Dict) -> str:
        memory_type = item.get("memory_type", "")
        subject = item.get("subject", "")
        value = item.get("value") or {}
        summary = value.get("summary")
        if summary:
            return str(summary)
        if memory_type == "user_identity":
            if value.get("preferred_name"):
                return f"A usuária prefere ser chamada de {value['preferred_name']}."
            if value.get("given_name"):
                return f"O nome da usuária é {value['given_name']}."
        if memory_type == "catalog_seen":
            return f"A usuária já viu {subject}."
        if memory_type in {"temporary_preference", "durable_preference"}:
            return json.dumps(value, ensure_ascii=False)
        return f"{memory_type}/{subject}: {json.dumps(value, ensure_ascii=False)}"

    def record_recall(self, query: str, results: Iterable[Dict]) -> None:
        now = utc_now()
        with sqlite3.connect(self.sqlite_path) as conn:
            for item in results:
                existing = conn.execute(
                    """
                    SELECT recall_count, total_score, max_score, promoted_at
                    FROM short_term_recall
                    WHERE item_key = ?
                    """,
                    (item["item_key"],),
                ).fetchone()
                if existing:
                    conn.execute(
                        """
                        UPDATE short_term_recall
                        SET recall_count = ?, total_score = ?, max_score = ?, last_recalled_at = ?
                        WHERE item_key = ?
                        """,
                        (
                            existing[0] + 1,
                            existing[1] + float(item.get("score", 1.0)),
                            max(existing[2], float(item.get("score", 1.0))),
                            now,
                            item["item_key"],
                        ),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO short_term_recall
                        (item_kind, item_key, source_ref, snippet, recall_count, total_score, max_score, first_recalled_at, last_recalled_at, promoted_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
                        """,
                        (
                            item["kind"],
                            item["item_key"],
                            item["source_ref"],
                            item["snippet"][:500],
                            1,
                            float(item.get("score", 1.0)),
                            float(item.get("score", 1.0)),
                            now,
                            now,
                        ),
                    )
            conn.commit()

    def promote_recalled_candidates(self, min_recall_count: int = 2) -> int:
        with sqlite3.connect(self.sqlite_path) as conn:
            rows = conn.execute(
                """
                SELECT r.item_key, r.recall_count, c.memory_type, c.subject, c.value_json, c.confidence, c.temporal_weight, c.expires_at
                FROM short_term_recall r
                JOIN memory_candidates c ON r.item_key = 'candidate:' || c.dedupe_key
                WHERE c.status = 'active' AND r.promoted_at IS NULL AND r.recall_count >= ?
                ORDER BY r.recall_count DESC, c.updated_at DESC
                """,
                (min_recall_count,),
            ).fetchall()
            if not rows:
                return 0
            now = utc_now()
            promoted = 0
            for row in rows:
                item_key, recall_count, memory_type, subject, value_json, confidence, temporal_weight, expires_at = row
                existing = conn.execute(
                    """
                    SELECT id, confidence, temporal_weight
                    FROM memory_items
                    WHERE memory_type = ? AND subject = ? AND status = 'active'
                    """,
                    (memory_type, subject),
                ).fetchone()
                if existing:
                    conn.execute(
                        """
                        UPDATE memory_items
                        SET value_json = ?, confidence = ?, temporal_weight = ?, source = ?, expires_at = ?, updated_at = ?
                        WHERE id = ?
                        """,
                        (
                            value_json,
                            max(existing[1], float(confidence)),
                            max(existing[2], float(temporal_weight)),
                            "promotion",
                            expires_at,
                            now,
                            existing[0],
                        ),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO memory_items
                        (memory_type, subject, value_json, confidence, temporal_weight, status, source, expires_at, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, 'active', 'promotion', ?, ?, ?)
                        """,
                        (
                            memory_type,
                            subject,
                            value_json,
                            confidence,
                            temporal_weight,
                            expires_at,
                            now,
                            now,
                        ),
                    )
                conn.execute(
                    "UPDATE short_term_recall SET promoted_at = ? WHERE item_key = ?",
                    (now, item_key),
                )
                promoted += 1
            conn.commit()
            return promoted

    def list_recent(self, limit: int = 20) -> List[Dict]:
        with sqlite3.connect(self.sqlite_path) as conn:
            durable_rows = conn.execute(
                """
                SELECT memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at
                FROM memory_items
                WHERE status = 'active'
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            candidate_rows = conn.execute(
                """
                SELECT memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at
                FROM memory_candidates
                WHERE status = 'active'
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        items = []
        for row in durable_rows:
            memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at = row
            items.append(
                {
                    "layer": "durable",
                    "memory_type": memory_type,
                    "subject": subject,
                    "value": json.loads(value_json),
                    "confidence": confidence,
                    "temporal_weight": temporal_weight,
                    "updated_at": updated_at,
                    "expires_at": expires_at,
                }
            )
        for row in candidate_rows:
            memory_type, subject, value_json, confidence, temporal_weight, updated_at, expires_at = row
            items.append(
                {
                    "layer": "candidate",
                    "memory_type": memory_type,
                    "subject": subject,
                    "value": json.loads(value_json),
                    "confidence": confidence,
                    "temporal_weight": temporal_weight,
                    "updated_at": updated_at,
                    "expires_at": expires_at,
                }
            )
        items.sort(key=lambda item: item["updated_at"], reverse=True)
        return items[:limit]

    @staticmethod
    def temporary_expiry(hours: int = 24) -> str:
        return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()

    def _fact_dedupe_key(self, fact: MemoryFact) -> str:
        canonical_value = self._canonicalize_fact_value(fact.memory_type, fact.subject, fact.value)
        seed = json.dumps(
            {
                "memory_type": fact.memory_type,
                "subject": fact.subject.strip().lower(),
                "value": canonical_value,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        return hashlib.sha1(seed.encode("utf-8")).hexdigest()

    def _drop_conflicting_identity_facts(self, conn: sqlite3.Connection, fact: MemoryFact) -> None:
        if fact.memory_type != "user_identity":
            return
        if fact.subject not in {"given_name", "preferred_name", "full_name"}:
            return
        canonical_value = self._canonicalize_fact_value(fact.memory_type, fact.subject, fact.value)
        conn.execute(
            """
            UPDATE memory_candidates
            SET status = 'superseded', updated_at = ?
            WHERE memory_type = ? AND subject = ? AND dedupe_key != ? AND status = 'active'
            """,
            (utc_now(), fact.memory_type, fact.subject, self._fact_dedupe_key(fact)),
        )
        rows = conn.execute(
            """
            SELECT id, value_json
            FROM memory_items
            WHERE memory_type = ? AND subject = ? AND status = 'active'
            """,
            (fact.memory_type, fact.subject),
        ).fetchall()
        for item_id, value_json in rows:
            try:
                existing_value = json.loads(value_json)
            except json.JSONDecodeError:
                continue
            existing_canonical = self._canonicalize_fact_value(fact.memory_type, fact.subject, existing_value)
            if existing_canonical != canonical_value:
                conn.execute(
                    """
                    UPDATE memory_items
                    SET status = 'superseded', updated_at = ?
                    WHERE id = ?
                    """,
                    (utc_now(), item_id),
                )

    def _supersede_memory_subject(self, conn: sqlite3.Connection, memory_type: str, subject: str, now: str) -> None:
        candidate_rows = conn.execute(
            """
            SELECT dedupe_key
            FROM memory_candidates
            WHERE memory_type = ? AND subject = ? AND status = 'active'
            """,
            (memory_type, subject),
        ).fetchall()
        for (dedupe_key,) in candidate_rows:
            item_key = f"candidate:{dedupe_key}"
            conn.execute(
                """
                UPDATE memory_candidates
                SET status = 'superseded', updated_at = ?
                WHERE dedupe_key = ?
                """,
                (now, dedupe_key),
            )
            conn.execute("DELETE FROM short_term_recall WHERE item_key = ?", (item_key,))

        durable_rows = conn.execute(
            """
            SELECT id
            FROM memory_items
            WHERE memory_type = ? AND subject = ? AND status = 'active'
            """,
            (memory_type, subject),
        ).fetchall()
        for (memory_id,) in durable_rows:
            conn.execute(
                """
                UPDATE memory_items
                SET status = 'superseded', updated_at = ?
                WHERE id = ?
                """,
                (now, memory_id),
            )
            conn.execute("DELETE FROM short_term_recall WHERE item_key = ?", (f"durable:{memory_id}",))

    @classmethod
    def _canonicalize_fact_value(cls, memory_type: str, subject: str, value: Dict) -> Dict:
        cleaned = cls._strip_summary_fields(value)
        if memory_type == "user_identity":
            for key in ("preferred_name", "given_name", "full_name"):
                raw = cleaned.get(key)
                if isinstance(raw, str) and raw.strip():
                    return {key: normalize_text(raw)}
        if cleaned == {} and isinstance(value.get("summary"), str) and value["summary"].strip():
            return {"summary": normalize_text(value["summary"])}
        return cleaned

    @classmethod
    def _strip_summary_fields(cls, value):
        if isinstance(value, dict):
            cleaned = {}
            for key, item in value.items():
                if key == "summary":
                    continue
                cleaned[key] = cls._strip_summary_fields(item)
            return cleaned
        if isinstance(value, list):
            return [cls._strip_summary_fields(item) for item in value]
        return value

    @staticmethod
    def _is_expired(expires_at: Optional[str], now: datetime) -> bool:
        if not expires_at:
            return False
        try:
            return datetime.fromisoformat(expires_at) < now
        except ValueError:
            return False

    @staticmethod
    def _build_searchable_text(subject: str, value: Dict) -> str:
        pieces = [subject]
        for field in ("summary", "preference", "preferred_name", "statement"):
            if isinstance(value.get(field), str):
                pieces.append(value[field])
        pieces.append(json.dumps(value, ensure_ascii=False))
        return normalize_text(" ".join(pieces))

    @staticmethod
    def _score_match(phrase: str, tokens: List[str], searchable: str) -> float:
        score = 0.0
        if not searchable:
            return 0.0
        if phrase and phrase in searchable:
            score += 4.0
        for token in tokens:
            if token in searchable:
                score += 1.25
        return score
