from __future__ import annotations

from pathlib import Path

from assistant_app.skills.conversation_history_tool import ConversationHistoryTool
from assistant_app.sessions.manager import SessionManager
from assistant_app.skills.history_tool import SkillHistoryTool
from assistant_app.skills.playwright_cli import PlaywrightCliSkill
from assistant_app.skills.registry import SkillRegistry


def build_skill_registry(
    skills_dir: Path,
    skill_artifacts_dir: Path,
    provider,
    session_manager: SessionManager,
    debug_log=None,
) -> SkillRegistry:
    workspace_root = skills_dir.parent
    handlers = {
        "playwright-browser": PlaywrightCliSkill(
            artifacts_dir=skill_artifacts_dir / "playwright-browser",
            workspace_root=workspace_root,
            provider=provider,
            debug_log=debug_log,
        ),
        "conversation-history": ConversationHistoryTool(session_manager=session_manager, provider=provider),
        "skill-history": SkillHistoryTool(session_manager=session_manager),
    }
    return SkillRegistry.load_from_dir(skills_dir, handlers)
