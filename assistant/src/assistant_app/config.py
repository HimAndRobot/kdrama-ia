from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppConfig:
    root_dir: Path
    data_dir: Path
    debug_dir: Path
    transcripts_dir: Path
    sqlite_path: Path
    codex_auth_path: Path
    codex_base_url: str
    openai_api_key: str
    openai_model: str


def load_config() -> AppConfig:
    root_dir = Path(__file__).resolve().parents[2]
    data_dir = root_dir / ".assistant-data"
    debug_dir = data_dir / "debug"
    transcripts_dir = data_dir / "transcripts"
    sqlite_path = data_dir / "assistant.db"
    return AppConfig(
        root_dir=root_dir,
        data_dir=data_dir,
        debug_dir=debug_dir,
        transcripts_dir=transcripts_dir,
        sqlite_path=sqlite_path,
        codex_auth_path=Path(os.getenv("CODEX_AUTH_JSON_PATH", str(Path.home() / ".codex" / "auth.json"))),
        codex_base_url=os.getenv("CODEX_BASE_URL", "https://chatgpt.com/backend-api/codex").rstrip("/"),
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini",
    )
