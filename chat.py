# CLI interface for the KDrama recommendation agent
from agent import run_agent


def on_thinking_token(cycle, token):
    print(token, end="", flush=True)


def on_thinking_done(cycle, text):
    print()


def on_content_token(cycle, token):
    print(token, end="", flush=True)


def on_tool(cycle, name, args, result=None):
    args_str = ", ".join(f"{k}={v!r}" for k, v in args.items())
    print(f"\n🔧 Ciclo {cycle} — {name}({args_str})")


def on_response(content):
    print(f"\n{'='*60}\n")


def on_cycle_start(cycle):
    print(f"\n--- Ciclo {cycle} ---")


def main():
    print("=== KDrama IA ===\n")

    while True:
        try:
            user_input = input("Você: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAté mais!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("sair", "exit", "quit"):
            print("Até mais!")
            break

        print()
        run_agent(
            user_input,
            provider="openai",
            on_thinking_token=on_thinking_token,
            on_thinking_done=on_thinking_done,
            on_content_token=on_content_token,
            on_tool=on_tool,
            on_response=on_response,
            on_cycle_start=on_cycle_start,
        )
        print()


if __name__ == "__main__":
    main()
