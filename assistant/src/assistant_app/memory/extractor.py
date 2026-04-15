from __future__ import annotations

import re
from typing import List

from assistant_app.contracts import MemoryFact
from assistant_app.memory.store import MemoryStore


SEEN_PATTERNS = [
    re.compile(r"\b(j[aá] vi|eu vi|already watched|i watched)\b\s*(?:isso|esse|essa|it)?\s*[:,-]?\s*(.+)?", re.I),
]

NAME_PATTERNS = [
    re.compile(r"\bme chamo\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ' -]{0,60})", re.I),
    re.compile(r"\bmeu nome [ée]\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ' -]{0,60})", re.I),
    re.compile(r"\bpode me chamar de\s+([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ' -]{0,60})", re.I),
]


def _clean_name(raw: str) -> str:
    name = raw.strip(" .,:;!?\"'()[]{}")
    parts = [part for part in re.split(r"\s+", name) if part]
    if not parts:
        return ""
    return " ".join(part.capitalize() for part in parts[:4])


def extract_memory_candidates(text: str) -> List[MemoryFact]:
    facts: List[MemoryFact] = []
    stripped = text.strip()
    lowered = stripped.lower()

    if "já vi" in lowered or "ja vi" in lowered:
        title_hint = stripped.split("já vi", 1)[-1].strip(" .:-") if "já vi" in lowered else stripped
        if title_hint:
            facts.append(
                MemoryFact(
                    memory_type="catalog_seen",
                    subject=title_hint[:120],
                    value={"seen": True},
                    confidence=0.95,
                    temporal_weight=1.0,
                    source="conversation",
                )
            )

    for pattern in NAME_PATTERNS:
        match = pattern.search(stripped)
        if not match:
            continue
        preferred_name = _clean_name(match.group(1))
        if preferred_name:
            facts.append(
                MemoryFact(
                    memory_type="user_identity",
                    subject="preferred_name",
                    value={"preferred_name": preferred_name},
                    confidence=0.98,
                    temporal_weight=1.0,
                    source="conversation",
                )
            )
        break

    if "não quero" in lowered or "nao quero" in lowered:
        preference = stripped
        facts.append(
            MemoryFact(
                memory_type="temporary_preference",
                subject=preference[:120],
                value={"preference": preference},
                confidence=0.7,
                temporal_weight=1.0,
                source="conversation",
                expires_at=MemoryStore.temporary_expiry(24),
            )
        )

    if "gosto de" in lowered:
        preference = stripped
        facts.append(
            MemoryFact(
                memory_type="episodic_preference",
                subject=preference[:120],
                value={"preference": preference},
                confidence=0.75,
                temporal_weight=0.8,
                source="conversation",
            )
        )

    return facts
