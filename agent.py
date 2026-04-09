# KDrama recommendation agent with streaming tool-calling loop
# Supports Ollama (local) and OpenAI GPT-5.4-mini
import json
import os
import requests
from dotenv import load_dotenv
from tools import TOOL_REGISTRY, TOOL_DEFINITIONS

load_dotenv(override=True)

OLLAMA_URL = "http://192.168.1.132:11434"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

PROVIDERS = {
    "ollama": {"model": "gemma4:e4b", "label": "Gemma 4 E4B (local)"},
    "openai": {"model": "gpt-5.4-mini", "label": "GPT-5.4 Mini (OpenAI)"},
}

MAX_CYCLES = 20
MAX_TOOL_RESULT_CHARS = 4000

SYSTEM_PROMPT = """You are an expert K-drama recommendation agent. You help users find dramas they'll love.

You have access to a database of dramas with details, reviews, and recommendations. You MUST use your tools to research before answering — never guess.

HOW TO WORK:
1. Start by understanding what the user wants
2. Use search_dramas to find matching dramas — it combines genre, tag, review keyword, and relation filters in ONE call
3. Use get_drama_details and get_drama_reviews to deep-dive into specific dramas (supports multiple titles at once)
4. For subjective requests (e.g. "competent police", "strong romance"), use search_reviews to search across all reviews
5. list_dramas is paginated — only use it to browse, prefer search_dramas for targeted queries
6. Think step by step. Each cycle, decide: do I need more info, or do I have enough?
7. When you have enough info, give your final recommendation with clear reasoning

IMPORTANT:
- Always base recommendations on actual data from the tools
- For subjective criteria, search reviews — they contain user opinions about specific aspects
- You can call multiple tools per cycle if needed. Be efficient but thorough
- When responding to the user, write in Portuguese (Brazilian)
- Explain WHY you're recommending each drama based on what you found
- NEVER repeat a tool call you already made — if you already searched and got few results, work with what you have
- If the database doesn't have many matches, say so honestly and recommend the best ones you found
- Aim to give your answer within 5-8 cycles. Don't keep searching if results aren't changing"""


def execute_tool(name, args):
    """Executes a tool with structured error handling and result truncation."""
    func = TOOL_REGISTRY.get(name)
    if not func:
        return json.dumps({"error": f"Unknown tool: {name}", "tool": name})
    try:
        result = str(func(**args))
        if len(result) > MAX_TOOL_RESULT_CHARS:
            result = result[:MAX_TOOL_RESULT_CHARS] + f"\n\n[truncated — {len(result)} chars total, showing first {MAX_TOOL_RESULT_CHARS}]"
        return result
    except Exception as e:
        return json.dumps({"error": str(e), "tool": name})


def _openai_tools():
    tools = []
    for td in TOOL_DEFINITIONS:
        f = td["function"]
        tools.append({
            "type": "function",
            "name": f["name"],
            "description": f["description"],
            "parameters": f["parameters"],
        })
    return tools


# === OLLAMA PROVIDER ===

def stream_ollama(messages):
    payload = {
        "model": PROVIDERS["ollama"]["model"],
        "messages": messages,
        "tools": TOOL_DEFINITIONS,
        "stream": True,
    }
    try:
        resp = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, stream=True, timeout=120)
        resp.raise_for_status()
    except Exception as e:
        yield ("stream_end", {"content": "", "thinking": "", "tool_calls": [], "usage": {}, "error": str(e)})
        return

    content = ""
    thinking = ""
    tool_calls = []
    was_thinking = False
    usage = {}

    for line in resp.iter_lines():
        if not line:
            continue
        chunk = json.loads(line)
        msg = chunk.get("message", {})

        if msg.get("thinking"):
            token = msg["thinking"]
            thinking += token
            was_thinking = True
            yield ("thinking_token", token)

        if msg.get("content"):
            token = msg["content"]
            if was_thinking:
                was_thinking = False
                yield ("thinking_done", thinking)
            content += token
            yield ("content_token", token)

        if msg.get("tool_calls"):
            if was_thinking:
                was_thinking = False
                yield ("thinking_done", thinking)
            tool_calls.extend(msg["tool_calls"])

        if chunk.get("done"):
            if was_thinking:
                yield ("thinking_done", thinking)
            usage = {
                "input": chunk.get("prompt_eval_count", 0),
                "output": chunk.get("eval_count", 0),
                "thinking": 0,
            }
            break

    yield ("stream_end", {"content": content, "thinking": thinking, "tool_calls": tool_calls, "usage": usage})


# === OPENAI PROVIDER ===

def stream_openai(messages):
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)

    openai_messages = []
    for m in messages:
        if m["role"] == "tool":
            openai_messages.append({"role": "user", "content": f"[Tool result]: {m['content']}"})
        elif m["role"] == "system":
            openai_messages.append({"role": "developer", "content": m["content"]})
        else:
            content = m.get("content", "")
            if content:
                openai_messages.append({"role": m["role"], "content": content})

    try:
        response = client.responses.create(
            model=PROVIDERS["openai"]["model"],
            input=openai_messages,
            tools=_openai_tools(),
            reasoning={"effort": "high", "summary": "auto"},
            stream=True,
        )
    except Exception as e:
        yield ("stream_end", {"content": "", "thinking": "", "tool_calls": [], "usage": {}, "error": str(e)})
        return

    content = ""
    thinking = ""
    tool_calls = []
    fc_args_buf = {}
    usage = {}
    thinking_emitted = False

    for event in response:
        if event.type == "response.reasoning_summary_text.delta":
            token = event.delta
            thinking += token
            yield ("thinking_token", token)

        elif event.type == "response.reasoning_summary_text.done":
            if not thinking_emitted:
                thinking_emitted = True
                yield ("thinking_done", thinking)

        elif event.type == "response.output_text.delta":
            token = event.delta
            content += token
            yield ("content_token", token)

        elif event.type == "response.function_call_arguments.done":
            fc_args_buf[event.item_id] = event.arguments

        elif event.type == "response.completed":
            for item in event.response.output:
                if item.type == "function_call":
                    args = fc_args_buf.get(item.id, item.arguments)
                    parsed = json.loads(args) if isinstance(args, str) else args
                    tool_calls.append({"function": {"name": item.name, "arguments": parsed}})
            u = event.response.usage
            reasoning_tokens = 0
            if u and hasattr(u, "output_tokens_details") and u.output_tokens_details:
                reasoning_tokens = getattr(u.output_tokens_details, "reasoning_tokens", 0)
            usage = {
                "input": u.input_tokens if u else 0,
                "output": u.output_tokens if u else 0,
                "thinking": reasoning_tokens,
            }
            break

    yield ("stream_end", {"content": content, "thinking": thinking, "tool_calls": tool_calls, "usage": usage})


# === AGENT LOOP ===

def run_agent(user_message, provider="ollama", history=None, on_thinking_token=None, on_thinking_done=None, on_content_token=None, on_tool=None, on_response=None, on_cycle_start=None, on_tokens=None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    if history:
        for h in history:
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})

    messages.append({"role": "user", "content": user_message})

    tokens = {"input": 0, "output": 0, "thinking": 0}
    stream_fn = stream_openai if provider == "openai" else stream_ollama
    content = ""
    dramas_found = set()
    calls_made = []

    def emit_tokens():
        if on_tokens:
            on_tokens(tokens)

    KEEP_RECENT_TOOLS = 4

    def microcompact():
        """Replaces old tool results with a short summary (first 2 lines).
        The model sees what was found without the full data."""
        tool_indices = [i for i, m in enumerate(messages) if m["role"] == "tool"]
        if len(tool_indices) <= KEEP_RECENT_TOOLS:
            return
        to_clear = tool_indices[:-KEEP_RECENT_TOOLS]
        for i in to_clear:
            content = messages[i]["content"]
            if content.startswith("[Compacted]"):
                continue
            lines = content.split("\n")
            summary_lines = [l for l in lines[:5] if l.strip()][:2]
            messages[i]["content"] = "[Compacted] " + " | ".join(summary_lines)

    for cycle in range(1, MAX_CYCLES + 1):
        is_last = cycle == MAX_CYCLES
        emit_tokens()
        microcompact()

        if on_cycle_start:
            on_cycle_start(cycle)

        if cycle > 1:
            found_list = ", ".join(dramas_found) if dramas_found else "none yet"
            calls_summary = "; ".join(calls_made[-10:])
            nudge = f"[Cycle {cycle}/{MAX_CYCLES}] Dramas found: {found_list}. Tools already called: {calls_summary}."
            if cycle >= 8:
                nudge += " You have enough data — give your answer NOW. Do not search more."
            if is_last:
                nudge += " THIS IS YOUR LAST CYCLE. Respond with your recommendation immediately. NO MORE TOOL CALLS."
            messages.append({"role": "system", "content": nudge})

        final = {}

        for event_type, data in stream_fn(messages):
            if event_type == "thinking_token" and on_thinking_token:
                on_thinking_token(cycle, data)
            elif event_type == "thinking_done" and on_thinking_done:
                on_thinking_done(cycle, data)
            elif event_type == "content_token" and on_content_token:
                on_content_token(cycle, data)
            elif event_type == "stream_end":
                final = data
                usage = data.get("usage", {})
                tokens["input"] += usage.get("input", 0)
                tokens["output"] += usage.get("output", 0)
                tokens["thinking"] += usage.get("thinking", 0)
                emit_tokens()

        tool_calls = final.get("tool_calls", [])
        content = final.get("content", "")

        if not tool_calls:
            if on_response:
                on_response(content)
            return content

        messages.append({"role": "assistant", "content": content, "tool_calls": tool_calls})

        for tc in tool_calls:
            func_name = tc["function"]["name"]
            func_args = tc["function"]["arguments"]

            tool_result = execute_tool(func_name, func_args)
            calls_made.append(f"{func_name}({json.dumps(func_args)[:60]})")

            if on_tool:
                on_tool(cycle, func_name, func_args, tool_result)

            for line in tool_result.split("\n"):
                if line.strip().startswith("- ") or line.strip().startswith("+ "):
                    title = line.split("—")[0].replace("- ", "").replace("+ ", "").strip()
                    if title and len(title) > 2:
                        dramas_found.add(title.split("(")[0].strip())

            messages.append({"role": "tool", "content": tool_result})

    if on_response:
        on_response(content)
    return content
