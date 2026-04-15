from __future__ import annotations

import uuid
from typing import Iterable, List

from assistant_app.contracts import RuntimeEvent, UserMessage
from assistant_app.debug_log import DebugLog
from assistant_app.jobs.queue import JobQueue
from assistant_app.memory.store import MemoryStore
from assistant_app.memory.turn_reflection import TurnReflectionExtractor
from assistant_app.policies.store import PolicyStore
from assistant_app.sessions.manager import SessionManager, utc_now
from assistant_app.skills.registry import SkillRegistry


class RuntimeService:
    def __init__(
        self,
        session_manager: SessionManager,
        memory_store: MemoryStore,
        policy_store: PolicyStore,
        skill_registry: SkillRegistry,
        provider,
        job_queue: JobQueue,
        debug_log: DebugLog,
    ) -> None:
        self.session_manager = session_manager
        self.memory_store = memory_store
        self.policy_store = policy_store
        self.skill_registry = skill_registry
        self.provider = provider
        self.job_queue = job_queue
        self.debug_log = debug_log
        self.turn_reflection = TurnReflectionExtractor(provider)
        self.history_cursors: dict[str, str] = {}

    def _history_cursor_for(self, session_key: str) -> str:
        cursor = self.history_cursors.get(session_key)
        if cursor:
            return cursor
        cursor = utc_now()
        self.history_cursors[session_key] = cursor
        return cursor

    def handle_message(self, message: UserMessage) -> Iterable[RuntimeEvent]:
        turn_id = str(uuid.uuid4())
        session = self.session_manager.get_or_create(message.session_key)
        self.job_queue.wait_for_idle(8.0)
        history_cursor_at = self._history_cursor_for(message.session_key)
        recent_history = self.session_manager.tail(session, limit=12, since_created_at=history_cursor_at)
        user_created_at = utc_now()

        self.session_manager.append_entry(
            session,
            {
                "type": "message",
                "role": "user",
                "turn_id": turn_id,
                "surface": message.surface,
                "text": message.text,
                "created_at": user_created_at,
            },
        )
        self.memory_store.index_transcript_entry(
            session_key=message.session_key,
            session_id=session.session_id,
            turn_id=turn_id,
            role="user",
            text=message.text,
            source_path=str(session.transcript_path),
            created_at=user_created_at,
        )

        yield RuntimeEvent("run_started", {"session_id": session.session_id, "turn_id": turn_id})
        yield RuntimeEvent("memory_recall_started", {})
        memory_context = self.memory_store.get_context_pack(message.session_key)
        recent_memories = memory_context.get("recent_memories") or []
        active_policies = self.policy_store.resolve_for_turn(message.text)
        self.memory_store.record_recall(message.text, recent_memories)
        self.debug_log.write(
            "recall",
            {
                "turn_id": turn_id,
                "message": message.text,
                "memory_context": memory_context,
                "active_policies": active_policies,
            },
        )
        yield RuntimeEvent("memory_recall_finished", {"count": len(recent_memories)})

        if recent_memories:
            yield RuntimeEvent("tool_call_started", {"skill": "memory_search"})
            yield RuntimeEvent("tool_call_finished", {"skill": "memory_search", "count": len(recent_memories)})

        assembled = []
        for chunk in self.provider.stream_generate(message.text, memory_context, active_policies, recent_history):
            assembled.append(chunk)
            yield RuntimeEvent("assistant_delta", {"text": chunk})

        final_text = "".join(assembled)
        assistant_created_at = utc_now()
        self.session_manager.append_entry(
            session,
            {
                "type": "message",
                "role": "assistant",
                "turn_id": turn_id,
                "text": final_text,
                "created_at": assistant_created_at,
            },
        )
        self.memory_store.index_transcript_entry(
            session_key=message.session_key,
            session_id=session.session_id,
            turn_id=turn_id,
            role="assistant",
            text=final_text,
            source_path=str(session.transcript_path),
            created_at=assistant_created_at,
        )

        updated_history = self.session_manager.tail(session, limit=16, since_created_at=history_cursor_at)
        self.job_queue.submit(lambda: self._post_turn_memory_pass(turn_id, message.text, final_text, active_policies, updated_history))
        yield RuntimeEvent("run_finished", {"session_id": session.session_id})

    def reset_session(self, session_key: str) -> str:
        session = self.session_manager.reset(session_key)
        self.history_cursors[session_key] = utc_now()
        return session.session_id

    def describe_session(self, session_key: str) -> dict:
        session = self.session_manager.get_or_create(session_key)
        history_cursor_at = self._history_cursor_for(session_key)
        tail = self.session_manager.tail(session)
        current_tail = self.session_manager.tail(session, since_created_at=history_cursor_at)
        return {
            "session_key": session.session_key,
            "session_id": session.session_id,
            "transcript_path": str(session.transcript_path),
            "history_cursor_at": history_cursor_at,
            "tail_count": len(tail),
            "current_tail_count": len(current_tail),
        }

    def list_memory(self) -> List[dict]:
        self.job_queue.wait_for_idle(8.0)
        return self.memory_store.list_recent()

    def list_policies(self) -> List[dict]:
        self.job_queue.wait_for_idle(8.0)
        return self.policy_store.list_recent()

    def flush_background(self, timeout_s: float = 15.0) -> bool:
        return self.job_queue.wait_for_idle(timeout_s)

    def _post_turn_memory_pass(self, turn_id: str, user_text: str, assistant_text: str, active_policies: List[dict], recent_history: List[dict]) -> None:
        memory_context = self.memory_store.get_context_pack("main")
        profile_source_entries = self.memory_store.list_profile_source_entries()
        extracted = self.turn_reflection.extract(
            user_text=user_text,
            assistant_text=assistant_text,
            active_policies=self.policy_store.list_active(),
            recent_history=recent_history,
            memory_profile=memory_context.get("profile") or {},
            profile_source_entries=profile_source_entries,
        )
        facts = extracted["memory_facts"]
        memory_operations = extracted.get("memory_operations") or []
        policies = extracted["policies"]
        profile_text = extracted.get("profile_text") or ""
        self.debug_log.write(
            "reflection",
            {
                "turn_id": turn_id,
                "user_text": user_text,
                "assistant_text": assistant_text,
                "recent_history": recent_history,
                "memory_profile": memory_context.get("profile") or {},
                "profile_source_entries": profile_source_entries,
                "raw": extracted["raw"],
                "memory_facts": [
                    {
                        "memory_type": fact.memory_type,
                        "subject": fact.subject,
                        "value": fact.value,
                        "confidence": fact.confidence,
                        "temporal_weight": fact.temporal_weight,
                        "operation": fact.operation,
                        "expires_at": fact.expires_at,
                    }
                    for fact in facts
                ],
                "memory_operations": memory_operations,
                "policies": policies,
                "profile_text": profile_text,
            },
        )
        self.memory_store.apply_memory_operations(memory_operations)
        self.memory_store.add_candidate_facts(facts)
        self.policy_store.upsert_policies(policies)
        self.policy_store.decay_stale_policies()
        self.memory_store.promote_recalled_candidates()
        if profile_text:
            self.memory_store.set_profile_text(profile_text, "main")
