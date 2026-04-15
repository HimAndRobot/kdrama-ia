from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List


@dataclass
class Skill:
    id: str
    description: str
    handler: Callable[..., dict]


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.id] = skill

    def get(self, skill_id: str) -> Skill:
        return self._skills[skill_id]

    def list_skills(self) -> List[Skill]:
        return list(self._skills.values())

