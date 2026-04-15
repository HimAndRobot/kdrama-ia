from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class UserMessage:
    session_key: str
    surface: str
    text: str
    attachments: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryFact:
    memory_type: str
    subject: str
    value: Dict[str, Any]
    confidence: float
    temporal_weight: float
    operation: str = "set"
    status: str = "active"
    source: str = "conversation"
    expires_at: Optional[str] = None


@dataclass
class RuntimeEvent:
    type: str
    data: Dict[str, Any] = field(default_factory=dict)
