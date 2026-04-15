from __future__ import annotations

import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS transcript_corpus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_key TEXT NOT NULL UNIQUE,
    session_key TEXT NOT NULL,
    session_id TEXT NOT NULL,
    turn_id TEXT NOT NULL,
    role TEXT NOT NULL,
    text TEXT NOT NULL,
    source_path TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memory_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    value_json TEXT NOT NULL,
    confidence REAL NOT NULL,
    temporal_weight REAL NOT NULL,
    status TEXT NOT NULL,
    source TEXT NOT NULL,
    expires_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS memory_evidence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_item_id INTEGER NOT NULL,
    session_key TEXT NOT NULL,
    turn_id TEXT NOT NULL,
    snippet TEXT NOT NULL,
    source_kind TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(memory_item_id) REFERENCES memory_items(id)
);

CREATE TABLE IF NOT EXISTS memory_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dedupe_key TEXT NOT NULL UNIQUE,
    memory_type TEXT NOT NULL,
    subject TEXT NOT NULL,
    value_json TEXT NOT NULL,
    confidence REAL NOT NULL,
    temporal_weight REAL NOT NULL,
    source TEXT NOT NULL,
    expires_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS short_term_recall (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_kind TEXT NOT NULL,
    item_key TEXT NOT NULL UNIQUE,
    source_ref TEXT NOT NULL,
    snippet TEXT NOT NULL,
    recall_count INTEGER NOT NULL,
    total_score REAL NOT NULL,
    max_score REAL NOT NULL,
    first_recalled_at TEXT NOT NULL,
    last_recalled_at TEXT NOT NULL,
    promoted_at TEXT
);

CREATE TABLE IF NOT EXISTS active_policies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dedupe_key TEXT NOT NULL UNIQUE,
    policy_type TEXT NOT NULL,
    policy_slot TEXT NOT NULL DEFAULT '',
    instruction TEXT NOT NULL,
    applies_to_json TEXT NOT NULL,
    priority REAL NOT NULL,
    active INTEGER NOT NULL,
    source TEXT NOT NULL,
    revision_count INTEGER NOT NULL DEFAULT 1,
    explicit_set_count INTEGER NOT NULL DEFAULT 0,
    explicit_reinforce_count INTEGER NOT NULL DEFAULT 0,
    explicit_correction_count INTEGER NOT NULL DEFAULT 0,
    successful_apply_count INTEGER NOT NULL DEFAULT 0,
    violation_count INTEGER NOT NULL DEFAULT 0,
    stale_decay_count INTEGER NOT NULL DEFAULT 0,
    last_signal_type TEXT,
    last_reinforced_at TEXT,
    last_violated_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS policy_signal_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_slot TEXT NOT NULL,
    signal_type TEXT NOT NULL,
    delta REAL NOT NULL,
    evidence_json TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS policy_review_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    policy_slot TEXT NOT NULL UNIQUE,
    reason TEXT NOT NULL,
    status TEXT NOT NULL,
    suggested_prompt TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS session_state (
    session_key TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
"""


def bootstrap_storage(sqlite_path: Path, transcripts_dir: Path, debug_dir: Path) -> None:
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    debug_dir.mkdir(parents=True, exist_ok=True)
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(sqlite_path) as conn:
        conn.executescript(SCHEMA)
        existing_columns = {
            row[1]
            for row in conn.execute("PRAGMA table_info(active_policies)").fetchall()
        }
        if "policy_slot" not in existing_columns:
            conn.execute("ALTER TABLE active_policies ADD COLUMN policy_slot TEXT NOT NULL DEFAULT ''")
        if "revision_count" not in existing_columns:
            conn.execute("ALTER TABLE active_policies ADD COLUMN revision_count INTEGER NOT NULL DEFAULT 1")
        for column, ddl in (
            ("explicit_set_count", "ALTER TABLE active_policies ADD COLUMN explicit_set_count INTEGER NOT NULL DEFAULT 0"),
            ("explicit_reinforce_count", "ALTER TABLE active_policies ADD COLUMN explicit_reinforce_count INTEGER NOT NULL DEFAULT 0"),
            ("explicit_correction_count", "ALTER TABLE active_policies ADD COLUMN explicit_correction_count INTEGER NOT NULL DEFAULT 0"),
            ("successful_apply_count", "ALTER TABLE active_policies ADD COLUMN successful_apply_count INTEGER NOT NULL DEFAULT 0"),
            ("violation_count", "ALTER TABLE active_policies ADD COLUMN violation_count INTEGER NOT NULL DEFAULT 0"),
            ("stale_decay_count", "ALTER TABLE active_policies ADD COLUMN stale_decay_count INTEGER NOT NULL DEFAULT 0"),
            ("last_signal_type", "ALTER TABLE active_policies ADD COLUMN last_signal_type TEXT"),
            ("last_reinforced_at", "ALTER TABLE active_policies ADD COLUMN last_reinforced_at TEXT"),
            ("last_violated_at", "ALTER TABLE active_policies ADD COLUMN last_violated_at TEXT"),
        ):
            if column not in existing_columns:
                conn.execute(ddl)
        conn.commit()
