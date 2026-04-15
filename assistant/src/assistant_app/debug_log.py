from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


class DebugLog:
    def __init__(self, debug_dir: Path) -> None:
        self.debug_dir = debug_dir
        self.debug_dir.mkdir(parents=True, exist_ok=True)

    def write(self, name: str, payload: Dict[str, Any]) -> None:
        path = self.debug_dir / f"{name}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
