# API server for the KDrama agent — streams SSE events in real-time
import json
import os
import re
import threading
import queue
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from agent import run_agent
from tools import _load_data, _find_drama

app = FastAPI(title="KDrama IA API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class ChatRequest(BaseModel):
    message: str
    history: list = []
    provider: str = "ollama"


def sse(event, data):
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


def extract_drama_names(text):
    _load_data()
    from tools import _dramas
    all_titles = {d.get("title", "").lower(): d.get("title", "") for d in _dramas}

    found = []
    seen = set()

    for pattern in [r"\*\*([^*]+)\*\*", r"\*([^*]+)\*"]:
        for m in re.findall(pattern, text):
            clean = re.sub(r"\s*\(.*?\)\s*$", "", m).strip()
            if clean and clean.lower() not in seen:
                seen.add(clean.lower())
                found.append(clean)

    for title_lower, title in all_titles.items():
        if title_lower not in seen and title_lower in text.lower():
            seen.add(title_lower)
            found.append(title)

    return found


def get_drama_card(title):
    _load_data()
    d = _find_drama(title)
    if not d:
        return None
    return {
        "title": d.get("title"),
        "subtitle": d.get("subtitle", ""),
        "url": d.get("url", ""),
        "genres": d.get("genres", []),
        "tags": (d.get("tags") or [])[:6],
        "synopsis": (d.get("synopsis") or "")[:300],
        "ranked": (d.get("details") or {}).get("Ranked", "?"),
        "episodes": (d.get("details") or {}).get("Episodes", "?"),
        "aired": (d.get("details") or {}).get("Aired", "?"),
        "cast": [c for c in (d.get("cast") or []) if len(c) > 1][:5],
        "reviewCount": len(d.get("reviews") or []),
    }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    q = queue.Queue()
    debug_log = {"message": req.message, "provider": req.provider, "events": []}

    def log_event(event, data):
        debug_log["events"].append({"event": event, "data": data})

    def on_cycle_start(cycle):
        log_event("cycle_start", {"cycle": cycle})
        q.put(sse("cycle_start", {"cycle": cycle}))

    def on_thinking_token(cycle, token):
        q.put(sse("thinking_token", {"cycle": cycle, "token": token}))

    def on_thinking_done(cycle, full_text):
        log_event("thinking_done", {"cycle": cycle, "text": full_text})
        q.put(sse("thinking_done", {"cycle": cycle, "text": full_text}))

    def on_content_token(cycle, token):
        q.put(sse("content_token", {"cycle": cycle, "token": token}))

    def on_tool(cycle, name, args, result=None):
        log_event("tool_call", {"cycle": cycle, "name": name, "args": args, "result": result[:2000] if result else None})
        q.put(sse("tool_call", {"cycle": cycle, "name": name, "args": args}))

    def on_tokens(tokens):
        debug_log["tokens"] = dict(tokens)
        q.put(sse("tokens", tokens))

    def on_response(content):
        log_event("response", {"text": content[:500]})
        names = extract_drama_names(content)
        cards = [get_drama_card(n) for n in names]
        cards = [c for c in cards if c]
        if cards:
            log_event("drama_cards", {"count": len(cards), "titles": [c["title"] for c in cards]})
            q.put(sse("drama_cards", {"cards": cards}))
        q.put(sse("response", {"text": content}))

    def save_debug():
        import time
        os.makedirs("data", exist_ok=True)
        ts = int(time.time())
        with open(f"data/debug_{ts}.json", "w", encoding="utf-8") as f:
            json.dump(debug_log, f, indent=2, ensure_ascii=False)

    def agent_thread():
        try:
            run_agent(
                req.message,
                provider=req.provider,
                history=req.history,
                on_thinking_token=on_thinking_token,
                on_thinking_done=on_thinking_done,
                on_content_token=on_content_token,
                on_tool=on_tool,
                on_response=on_response,
                on_cycle_start=on_cycle_start,
                on_tokens=on_tokens,
            )
        except Exception as e:
            log_event("error", {"message": str(e)})
            q.put(sse("error", {"message": str(e)}))
        finally:
            save_debug()
            q.put(None)

    t = threading.Thread(target=agent_thread)
    t.start()

    def generate():
        while True:
            item = q.get()
            if item is None:
                yield sse("done", {})
                break
            yield item

    return StreamingResponse(generate(), media_type="text/event-stream")


@app.get("/api/providers")
async def providers():
    from agent import PROVIDERS, OPENAI_API_KEY
    available = []
    available.append({"id": "ollama", "label": PROVIDERS["ollama"]["label"], "model": PROVIDERS["ollama"]["model"]})
    if OPENAI_API_KEY:
        available.append({"id": "openai", "label": PROVIDERS["openai"]["label"], "model": PROVIDERS["openai"]["model"]})
    return {"providers": available}


app.mount("/static", StaticFiles(directory="web"), name="static")


@app.get("/")
async def index():
    return FileResponse("web/index.html")
