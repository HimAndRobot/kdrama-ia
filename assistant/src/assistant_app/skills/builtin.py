from __future__ import annotations

from assistant_app.memory.store import MemoryStore
from assistant_app.skills.registry import Skill, SkillRegistry


def build_builtin_skills(memory_store: MemoryStore) -> SkillRegistry:
    registry = SkillRegistry()

    def memory_search(query: str) -> dict:
        return {"items": memory_store.search(query)}

    def memory_list() -> dict:
        return {"items": memory_store.list_recent()}

    registry.register(Skill(id="memory_search", description="Search recalled memory facts", handler=memory_search))
    registry.register(Skill(id="memory_list", description="List recent memory items", handler=memory_list))
    return registry
