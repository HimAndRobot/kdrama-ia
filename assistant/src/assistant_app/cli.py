from __future__ import annotations

import json
import os
from pathlib import Path

from assistant_app.config import load_config
from assistant_app.contracts import UserMessage
from assistant_app.debug_log import DebugLog
from assistant_app.jobs.queue import JobQueue
from assistant_app.llm.provider import CodexProvider, LocalFallbackProvider, OpenAIProvider
from assistant_app.memory.store import MemoryStore
from assistant_app.policies.store import PolicyStore
from assistant_app.runtime.service import RuntimeService
from assistant_app.sessions.manager import SessionManager
from assistant_app.skills.builtin import build_builtin_skills
from assistant_app.storage.bootstrap import bootstrap_storage


def _has_codex_auth_material(cfg) -> bool:
    if os.getenv("CODEX_API_KEY", "").strip():
        return True
    return cfg.codex_auth_path.exists()


def build_runtime() -> tuple[RuntimeService, str]:
    cfg = load_config()
    bootstrap_storage(cfg.sqlite_path, cfg.transcripts_dir, cfg.debug_dir)
    session_manager = SessionManager(cfg.sqlite_path, cfg.transcripts_dir)
    memory_store = MemoryStore(cfg.sqlite_path)
    policy_store = PolicyStore(cfg.sqlite_path)
    debug_log = DebugLog(cfg.debug_dir)
    registry = build_builtin_skills(memory_store)
    if _has_codex_auth_material(cfg):
        provider = CodexProvider(cfg.codex_auth_path, cfg.codex_base_url)
        provider_name = "codex"
    elif cfg.openai_api_key:
        provider = OpenAIProvider(cfg.openai_api_key, cfg.openai_model) if cfg.openai_api_key else LocalFallbackProvider()
        provider_name = "openai"
    else:
        provider = LocalFallbackProvider()
        provider_name = "local-fallback"
    job_queue = JobQueue()
    return RuntimeService(session_manager, memory_store, policy_store, registry, provider, job_queue, debug_log), provider_name


def print_help() -> None:
    print("/help      mostra esta ajuda")
    print("/reset     inicia uma nova sessão")
    print("/session   mostra informações da sessão")
    print("/memory    lista a memória recente")
    print("/policies  lista as políticas ativas")
    print("/quit      sai")


def run_cli() -> None:
    runtime, provider_name = build_runtime()
    session_key = "main"

    print("Assistant")
    print("Sessão: main")
    print(f"Provider: {provider_name}")
    print("Digite /help para comandos.\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            runtime.flush_background()
            print("\nEncerrando.")
            break

        if not user_input:
            continue
        if user_input == "/help":
            print_help()
            continue
        if user_input == "/quit":
            runtime.flush_background()
            print("Encerrando.")
            break
        if user_input == "/reset":
            session_id = runtime.reset_session(session_key)
            print(f"Nova sessão criada: {session_id}")
            continue
        if user_input == "/session":
            print(json.dumps(runtime.describe_session(session_key), ensure_ascii=False, indent=2))
            continue
        if user_input == "/memory":
            print(json.dumps(runtime.list_memory(), ensure_ascii=False, indent=2))
            continue
        if user_input == "/policies":
            print(json.dumps(runtime.list_policies(), ensure_ascii=False, indent=2))
            continue

        message = UserMessage(session_key=session_key, surface="terminal", text=user_input)
        print("")
        try:
            for event in runtime.handle_message(message):
                if event.type == "memory_recall_started":
                    print("[memory] buscando contexto...")
                elif event.type == "memory_recall_finished":
                    print(f"[memory] {event.data['count']} item(ns) relevantes")
                elif event.type == "tool_call_started":
                    print(f"[skill] {event.data['skill']} iniciado")
                elif event.type == "tool_call_finished":
                    print(f"[skill] {event.data['skill']} concluído")
                elif event.type == "assistant_delta":
                    print(event.data["text"], end="", flush=True)
                elif event.type == "run_finished":
                    print("\n")
        except Exception as error:
            print(f"[erro] {error}\n")
