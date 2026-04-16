from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


@dataclass
class SkillExecutionContext:
    session_key: str
    user_message: str
    goal: str
    turn_id: str = ""
    debug_log: Any | None = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillRunResult:
    skill_id: str
    goal: str
    summary: str
    payload: Dict


SkillHandler = Callable[[SkillExecutionContext], SkillRunResult]


@dataclass
class Skill:
    id: str
    name: str
    description: str
    file_path: Path
    handler: SkillHandler
    operations: List[Dict[str, Any]] = field(default_factory=list)


def _strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _parse_frontmatter(skill_file: Path) -> Dict[str, str]:
    text = skill_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"SKILL.md sem frontmatter: {skill_file}")

    parsed: Dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        parsed[key.strip()] = _strip_quotes(raw_value)
    return parsed


def format_skills_for_prompt(skills: List[Skill]) -> str:
    if not skills:
        return ""

    lines = [
        "As skills abaixo fornecem capacidades locais sob demanda.",
        "Escolha no máximo uma skill quando ela realmente for necessária para executar trabalho externo antes da resposta.",
        "",
        "<available_skills>",
    ]
    for skill in skills:
        lines.append("  <skill>")
        lines.append(f"    <name>{skill.id}</name>")
        lines.append(f"    <description>{skill.description}</description>")
        lines.append(f"    <location>{skill.file_path}</location>")
        operations = skill.operations or []
        if operations:
            lines.append("    <operations>")
            for operation in operations:
                op_name = str(operation.get("op", "")).strip()
                if not op_name:
                    continue
                lines.append("      <operation>")
                lines.append(f"        <op>{op_name}</op>")
                description = str(operation.get("description", "")).strip()
                if description:
                    lines.append(f"        <description>{description}</description>")
                precondition = str(operation.get("precondition", "")).strip()
                if precondition:
                    lines.append(f"        <precondition>{precondition}</precondition>")
                params = operation.get("params")
                if params:
                    lines.append(f"        <params>{params}</params>")
                lines.append("      </operation>")
            lines.append("    </operations>")
        lines.append("  </skill>")
    lines.append("</available_skills>")
    return "\n".join(lines)


class SkillRegistry:
    def __init__(self) -> None:
        self._skills: Dict[str, Skill] = {}

    def register(self, skill: Skill) -> None:
        self._skills[skill.id] = skill

    def get(self, skill_id: str) -> Optional[Skill]:
        return self._skills.get(skill_id)

    def list_skills(self) -> List[Skill]:
        return list(self._skills.values())

    def format_for_prompt(self) -> str:
        return format_skills_for_prompt(self.list_skills())

    @classmethod
    def load_from_dir(cls, skills_dir: Path, handlers: Dict[str, SkillHandler]) -> "SkillRegistry":
        registry = cls()
        if not skills_dir.exists():
            return registry

        for entry in sorted(skills_dir.iterdir()):
            if not entry.is_dir():
                continue
            skill_file = entry / "SKILL.md"
            if not skill_file.exists():
                continue
            metadata = _parse_frontmatter(skill_file)
            skill_id = metadata.get("name", entry.name).strip() or entry.name
            handler = handlers.get(skill_id)
            if handler is None:
                continue
            registry.register(
                Skill(
                    id=skill_id,
                    name=metadata.get("title", skill_id),
                    description=metadata.get("description", "").strip(),
                    file_path=skill_file,
                    handler=handler,
                    operations=list(getattr(handler, "describe_operations", lambda: [])()),
                )
            )
        return registry
