from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List


SIGNAL_DELTAS = {
    "explicit_set": 0.0,
    "explicit_reinforce": 0.15,
    "explicit_correction": 0.2,
    "successful_apply": 0.03,
    "violation": 0.2,
    "stale_decay": -0.02,
    "downgrade": -0.08,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_text(value: str) -> str:
    return " ".join(value.lower().split())


class PolicyStore:
    def __init__(self, sqlite_path: Path) -> None:
        self.sqlite_path = sqlite_path

    def upsert_policies(self, policies: List[Dict]) -> None:
        if not policies:
            return
        now = utc_now()
        with sqlite3.connect(self.sqlite_path) as conn:
            for policy in policies:
                slot = policy["policy_slot"].strip().lower()
                operation = policy.get("operation", "set")
                dedupe_key = self._dedupe_key(policy)
                applies_to_json = json.dumps(policy.get("applies_to") or {}, ensure_ascii=False, sort_keys=True)
                existing = conn.execute(
                    """
                    SELECT id, dedupe_key, priority, revision_count, active,
                           explicit_set_count, explicit_reinforce_count, explicit_correction_count,
                           successful_apply_count, violation_count, stale_decay_count
                    FROM active_policies
                    WHERE policy_slot = ?
                    ORDER BY updated_at DESC
                    LIMIT 1
                    """,
                    (slot,),
                ).fetchone()

                if operation == "deactivate":
                    conn.execute(
                        """
                        UPDATE active_policies
                        SET active = 0, updated_at = ?, last_signal_type = ?
                        WHERE policy_slot = ? AND active = 1
                        """,
                        (now, "deactivate", slot),
                    )
                    self._record_signal(
                        conn,
                        slot,
                        "deactivate",
                        0.0,
                        {"instruction": policy.get("instruction", ""), "operation": operation},
                        now,
                    )
                    continue

                if existing:
                    (
                        policy_id,
                        existing_key,
                        existing_priority,
                        revision_count,
                        active,
                        explicit_set_count,
                        explicit_reinforce_count,
                        explicit_correction_count,
                        successful_apply_count,
                        violation_count,
                        stale_decay_count,
                    ) = existing
                    signal_type = self._resolve_signal_type(operation, existing_key == dedupe_key)
                    new_priority = self._apply_delta(float(existing_priority), SIGNAL_DELTAS[signal_type])
                    counters = self._next_counters(
                        explicit_set_count=int(explicit_set_count),
                        explicit_reinforce_count=int(explicit_reinforce_count),
                        explicit_correction_count=int(explicit_correction_count),
                        successful_apply_count=int(successful_apply_count),
                        violation_count=int(violation_count),
                        stale_decay_count=int(stale_decay_count),
                        signal_type=signal_type,
                    )
                    conn.execute(
                        """
                        UPDATE active_policies
                        SET dedupe_key = ?, policy_type = ?, policy_slot = ?, instruction = ?, applies_to_json = ?,
                            priority = ?, active = ?, source = ?, revision_count = ?, explicit_set_count = ?,
                            explicit_reinforce_count = ?, explicit_correction_count = ?, successful_apply_count = ?,
                            violation_count = ?, stale_decay_count = ?, last_signal_type = ?, last_reinforced_at = ?,
                            last_violated_at = ?, updated_at = ?
                        WHERE id = ?
                        """,
                        (
                            dedupe_key,
                            policy["policy_type"],
                            slot,
                            policy["instruction"],
                            applies_to_json,
                            new_priority,
                            1 if policy.get("active", True) else 0,
                            policy.get("source", "reflection"),
                            int(revision_count) + (1 if operation in {"replace", "downgrade"} else 0),
                            counters["explicit_set_count"],
                            counters["explicit_reinforce_count"],
                            counters["explicit_correction_count"],
                            counters["successful_apply_count"],
                            counters["violation_count"],
                            counters["stale_decay_count"],
                            signal_type,
                            now if signal_type in {"explicit_reinforce", "explicit_correction"} else None,
                            now if signal_type == "violation" else None,
                            now,
                            policy_id,
                        ),
                    )
                    self._record_signal(
                        conn,
                        slot,
                        signal_type,
                        SIGNAL_DELTAS[signal_type],
                        {
                            "instruction": policy["instruction"],
                            "operation": operation,
                            "policy_type": policy["policy_type"],
                            "same_as_existing": existing_key == dedupe_key,
                        },
                        now,
                    )
                    continue

                conn.execute(
                    """
                    INSERT INTO active_policies
                    (dedupe_key, policy_type, policy_slot, instruction, applies_to_json, priority, active, source,
                     revision_count, explicit_set_count, explicit_reinforce_count, explicit_correction_count,
                     successful_apply_count, violation_count, stale_decay_count, last_signal_type, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        dedupe_key,
                        policy["policy_type"],
                        slot,
                        policy["instruction"],
                        applies_to_json,
                        0.0,
                        1 if policy.get("active", True) else 0,
                        policy.get("source", "reflection"),
                        1,
                        1,
                        0,
                        0,
                        0,
                        0,
                        0,
                        "explicit_set",
                        now,
                        now,
                    ),
                )
                self._record_signal(
                    conn,
                    slot,
                    "explicit_set",
                    SIGNAL_DELTAS["explicit_set"],
                    {
                        "instruction": policy["instruction"],
                        "operation": operation,
                        "policy_type": policy["policy_type"],
                    },
                    now,
                )
            conn.commit()

    def record_policy_success(self, active_policies: List[Dict], assistant_text: str) -> None:
        if not active_policies:
            return
        now = utc_now()
        with sqlite3.connect(self.sqlite_path) as conn:
            for policy in active_policies:
                slot = str(policy.get("policy_slot", "")).strip().lower()
                if not slot:
                    continue
                row = conn.execute(
                    """
                    SELECT id, priority, successful_apply_count
                    FROM active_policies
                    WHERE policy_slot = ? AND active = 1
                    ORDER BY updated_at DESC
                    LIMIT 1
                    """,
                    (slot,),
                ).fetchone()
                if not row:
                    continue
                policy_id, priority, successful_apply_count = row
                new_priority = self._apply_delta(float(priority), SIGNAL_DELTAS["successful_apply"])
                conn.execute(
                    """
                    UPDATE active_policies
                    SET priority = ?, successful_apply_count = ?, last_signal_type = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (new_priority, int(successful_apply_count) + 1, "successful_apply", now, policy_id),
                )
                self._record_signal(
                    conn,
                    slot,
                    "successful_apply",
                    SIGNAL_DELTAS["successful_apply"],
                    {"assistant_text": assistant_text[:300]},
                    now,
                )
            conn.commit()

    def decay_stale_policies(self, stale_after_hours: int = 72) -> None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=stale_after_hours)
        cutoff_iso = cutoff.isoformat()
        now = utc_now()
        with sqlite3.connect(self.sqlite_path) as conn:
            rows = conn.execute(
                """
                SELECT id, policy_slot, priority, stale_decay_count
                FROM active_policies
                WHERE active = 1 AND updated_at < ?
                """,
                (cutoff_iso,),
            ).fetchall()
            for policy_id, slot, priority, stale_decay_count in rows:
                new_priority = self._apply_delta(float(priority), SIGNAL_DELTAS["stale_decay"])
                conn.execute(
                    """
                    UPDATE active_policies
                    SET priority = ?, stale_decay_count = ?, last_signal_type = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (new_priority, int(stale_decay_count) + 1, "stale_decay", now, policy_id),
                )
                self._record_signal(
                    conn,
                    slot,
                    "stale_decay",
                    SIGNAL_DELTAS["stale_decay"],
                    {"stale_after_hours": stale_after_hours},
                    now,
                )
                if new_priority <= 0.0:
                    self._queue_review(
                        conn,
                        slot,
                        "zero_weight_stale",
                        "Você quer que eu remova ou atualize essa regra?",
                        now,
                    )
            conn.commit()

    def resolve_for_turn(self, message_text: str) -> List[Dict]:
        with sqlite3.connect(self.sqlite_path) as conn:
            rows = conn.execute(
                """
                SELECT policy_type, policy_slot, instruction, applies_to_json, priority, active, updated_at, revision_count
                FROM active_policies
                WHERE active = 1
                ORDER BY priority DESC, updated_at DESC
                """
            ).fetchall()
        resolved: List[Dict] = []
        for row in rows:
            policy_type, policy_slot, instruction, applies_to_json, priority, active, updated_at, revision_count = row
            applies_to = json.loads(applies_to_json) if applies_to_json else {}
            resolved.append(
                {
                    "policy_type": policy_type,
                    "policy_slot": policy_slot,
                    "instruction": instruction,
                    "applies_to": applies_to,
                    "priority": priority,
                    "matched": "candidate",
                    "revision_count": revision_count,
                }
            )
        return resolved

    def list_recent(self, limit: int = 20) -> List[dict]:
        with sqlite3.connect(self.sqlite_path) as conn:
            rows = conn.execute(
                """
                SELECT policy_type, policy_slot, instruction, applies_to_json, priority, active, revision_count,
                       explicit_set_count, explicit_reinforce_count, explicit_correction_count,
                       successful_apply_count, violation_count, stale_decay_count, updated_at
                FROM active_policies
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        items = []
        for row in rows:
            (
                policy_type,
                policy_slot,
                instruction,
                applies_to_json,
                priority,
                active,
                revision_count,
                explicit_set_count,
                explicit_reinforce_count,
                explicit_correction_count,
                successful_apply_count,
                violation_count,
                stale_decay_count,
                updated_at,
            ) = row
            items.append(
                {
                    "policy_type": policy_type,
                    "policy_slot": policy_slot,
                    "instruction": instruction,
                    "applies_to": json.loads(applies_to_json) if applies_to_json else {},
                    "priority": priority,
                    "active": bool(active),
                    "revision_count": revision_count,
                    "signals": {
                        "explicit_set_count": explicit_set_count,
                        "explicit_reinforce_count": explicit_reinforce_count,
                        "explicit_correction_count": explicit_correction_count,
                        "successful_apply_count": successful_apply_count,
                        "violation_count": violation_count,
                        "stale_decay_count": stale_decay_count,
                    },
                    "updated_at": updated_at,
                }
            )
        return items

    def list_active(self) -> List[Dict]:
        with sqlite3.connect(self.sqlite_path) as conn:
            rows = conn.execute(
                """
                SELECT policy_type, policy_slot, instruction, applies_to_json, priority, revision_count
                FROM active_policies
                WHERE active = 1
                ORDER BY priority DESC, updated_at DESC
                """
            ).fetchall()
        items = []
        for row in rows:
            policy_type, policy_slot, instruction, applies_to_json, priority, revision_count = row
            items.append(
                {
                    "policy_type": policy_type,
                    "policy_slot": policy_slot,
                    "instruction": instruction,
                    "applies_to": json.loads(applies_to_json) if applies_to_json else {},
                    "priority": priority,
                    "revision_count": revision_count,
                }
            )
        return items

    @staticmethod
    def _apply_delta(current: float, delta: float) -> float:
        return max(0.0, min(1.0, current + delta))

    @staticmethod
    def _resolve_signal_type(operation: str, same_as_existing: bool) -> str:
        if operation == "downgrade":
            return "downgrade"
        if operation == "replace":
            return "explicit_correction"
        if same_as_existing:
            return "explicit_reinforce"
        return "explicit_set"

    @staticmethod
    def _next_counters(
        *,
        explicit_set_count: int,
        explicit_reinforce_count: int,
        explicit_correction_count: int,
        successful_apply_count: int,
        violation_count: int,
        stale_decay_count: int,
        signal_type: str,
    ) -> Dict[str, int]:
        counters = {
            "explicit_set_count": explicit_set_count,
            "explicit_reinforce_count": explicit_reinforce_count,
            "explicit_correction_count": explicit_correction_count,
            "successful_apply_count": successful_apply_count,
            "violation_count": violation_count,
            "stale_decay_count": stale_decay_count,
        }
        if signal_type in counters:
            counters[signal_type] += 1
        return counters

    def _record_signal(
        self,
        conn: sqlite3.Connection,
        policy_slot: str,
        signal_type: str,
        delta: float,
        evidence: Dict,
        created_at: str,
    ) -> None:
        conn.execute(
            """
            INSERT INTO policy_signal_events (policy_slot, signal_type, delta, evidence_json, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (policy_slot, signal_type, delta, json.dumps(evidence, ensure_ascii=False), created_at),
        )

    def _queue_review(
        self,
        conn: sqlite3.Connection,
        policy_slot: str,
        reason: str,
        suggested_prompt: str,
        now: str,
    ) -> None:
        conn.execute(
            """
            INSERT INTO policy_review_queue (policy_slot, reason, status, suggested_prompt, created_at, updated_at)
            VALUES (?, ?, 'pending', ?, ?, ?)
            ON CONFLICT(policy_slot) DO UPDATE SET
                reason = excluded.reason,
                status = 'pending',
                suggested_prompt = excluded.suggested_prompt,
                updated_at = excluded.updated_at
            """,
            (policy_slot, reason, suggested_prompt, now, now),
        )

    @staticmethod
    def _dedupe_key(policy: Dict) -> str:
        payload = json.dumps(
            {
                "policy_type": policy["policy_type"],
                "policy_slot": policy["policy_slot"].strip().lower(),
                "instruction": policy.get("instruction", "").strip().lower(),
                "applies_to": policy.get("applies_to") or {},
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        return hashlib.sha1(payload.encode("utf-8")).hexdigest()
