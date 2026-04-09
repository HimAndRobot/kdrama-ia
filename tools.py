# Tool implementations for the KDrama recommendation agent
import json
import re
from pathlib import Path

DB_FILE = Path("./data/db.json")

_dramas = []


def _load_data():
    global _dramas
    if not DB_FILE.exists():
        _dramas = []
        return
    with open(DB_FILE, "r", encoding="utf-8") as f:
        _dramas = json.load(f)


def _find_drama(title):
    title_lower = title.lower().strip()
    for d in _dramas:
        if d.get("title", "").lower() == title_lower:
            return d
    for d in _dramas:
        if title_lower in d.get("title", "").lower():
            return d
    return None


def _extract_snippet(text, terms):
    text_lower = text.lower()
    best_pos = len(text)
    for t in terms:
        pos = text_lower.find(t)
        if pos != -1 and pos < best_pos:
            best_pos = pos
    start = max(0, best_pos - 80)
    end = min(len(text), best_pos + 200)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


def _drama_summary(d):
    genres = ", ".join(d.get("genres", []))
    tags = ", ".join((d.get("tags") or [])[:6])
    ranked = (d.get("details") or {}).get("Ranked", "?")
    eps = (d.get("details") or {}).get("Episodes", "?")
    n_rev = len(d.get("reviews") or [])
    return f"{d.get('title')} ({d.get('subtitle', '')}) — {genres} — Tags: {tags} — Ranked {ranked} — {eps} eps — {n_rev} reviews"


# === TOOLS ===


def list_dramas(page=1, per_page=20):
    """Returns a paginated summary of dramas in the database."""
    _load_data()
    total = len(_dramas)
    total_pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = min(start + per_page, total)
    lines = [f"Page {page}/{total_pages} ({total} dramas total):"]
    for i, d in enumerate(_dramas[start:end], start + 1):
        lines.append(f"  {i}. {_drama_summary(d)}")
    if page < total_pages:
        lines.append(f"\n(Use page={page + 1} to see more)")
    return "\n".join(lines)


def search_dramas(genres=None, tags=None, related_to=None, keywords_in_reviews=None, exclude=None):
    """Powerful combined search. All filters are AND-combined. Returns matching dramas with summaries."""
    _load_data()
    results = list(_dramas)

    if genres:
        genre_list = [g.strip().lower() for g in genres.split(",")]
        results = [d for d in results if any(g in gl.lower() for g in genre_list for gl in d.get("genres", []))]

    if tags:
        tag_list = [t.strip().lower() for t in tags.split(",")]
        results = [d for d in results if any(t in tl.lower() for t in tag_list for tl in d.get("tags", []))]

    if related_to:
        ref = _find_drama(related_to)
        if ref:
            rec_urls = {r.get("url", "") for r in ref.get("recommendations", [])}
            rec_titles = {r.get("title", "").lower() for r in ref.get("recommendations", [])}
            results = [d for d in results if d.get("url") in rec_urls or d.get("title", "").lower() in rec_titles]

    if keywords_in_reviews:
        terms = [k.strip().lower() for k in keywords_in_reviews.split(",")]
        filtered = []
        for d in results:
            for r in d.get("reviews", []):
                content = (r.get("content") or "").lower()
                if any(t in content for t in terms):
                    filtered.append(d)
                    break
        results = filtered

    if exclude:
        exc_list = [e.strip().lower() for e in exclude.split(",")]
        results = [d for d in results if d.get("title", "").lower() not in exc_list]

    if not results:
        return "No dramas found matching all criteria."

    lines = [f"Found {len(results)} drama(s):"]
    for d in results:
        lines.append(f"  - {_drama_summary(d)}")
    return "\n".join(lines)


def get_drama_details(titles):
    """Returns full details of one or more dramas. Comma-separate multiple titles."""
    _load_data()
    title_list = [t.strip() for t in titles.split(",")]
    parts = []

    for title in title_list:
        d = _find_drama(title)
        if not d:
            parts.append(f"\n--- {title}: NOT FOUND ---")
            continue

        det = d.get("details") or {}
        recs = d.get("recommendations", [])
        cast = [c for c in (d.get("cast") or []) if len(c) > 1][:8]

        block = [
            f"\n--- {d.get('title')} ---",
            f"Info: {d.get('subtitle', '')}",
            f"Genres: {', '.join(d.get('genres', []))}",
            f"Tags: {', '.join(d.get('tags', []))}",
            f"Cast: {', '.join(cast)}",
            f"Synopsis: {d.get('synopsis', 'N/A')}",
        ]
        for k in ["Episodes", "Aired", "Duration", "Country", "Original Network", "Ranked", "Popularity"]:
            if k in det:
                val = det[k] if isinstance(det[k], str) else ", ".join(det[k])
                block.append(f"{k}: {val}")
        if recs:
            block.append(f"MDL recommendations: {', '.join(r.get('title', '') for r in recs[:10])}")

        parts.append("\n".join(block))

    return "\n".join(parts)


def get_drama_reviews(titles, limit=3, keywords=None):
    """Returns reviews for one or more dramas. Optionally filter by keywords."""
    _load_data()
    title_list = [t.strip() for t in titles.split(",")]
    terms = [k.strip().lower() for k in keywords.split(",")] if keywords else []
    parts = []

    for title in title_list:
        d = _find_drama(title)
        if not d:
            parts.append(f"\n--- {title}: NOT FOUND ---")
            continue

        reviews = d.get("reviews") or []
        if terms:
            reviews = [r for r in reviews if any(t in (r.get("content") or "").lower() for t in terms)]

        if not reviews:
            parts.append(f"\n--- {d.get('title')}: no {'matching ' if terms else ''}reviews ---")
            continue

        block = [f"\n--- {d.get('title')} ({len(reviews)} {'matching ' if terms else ''}reviews, showing {min(limit, len(reviews))}) ---"]
        for r in reviews[:limit]:
            content = (r.get("content") or "")[:600]
            if terms:
                content = _extract_snippet(r.get("content") or "", terms)
            block.append(f"  [{r.get('author', '?')} ★{r.get('overall', '?')}] {content}")

        parts.append("\n".join(block))

    return "\n".join(parts)


def search_reviews(keywords, limit=8):
    """Searches ALL reviews across ALL dramas for keywords. Essential for subjective queries."""
    _load_data()
    terms = [k.strip().lower() for k in keywords.split(",")]
    results = []

    for d in _dramas:
        for r in d.get("reviews") or []:
            content = (r.get("content") or "").lower()
            matched = [t for t in terms if t in content]
            if matched:
                snippet = _extract_snippet(r.get("content") or "", terms)
                results.append(f"  [{d.get('title')}] {r.get('author', '?')} ★{r.get('overall', '?')} — matched: {', '.join(matched)}\n    \"{snippet}\"")

    if not results:
        return f"No reviews mention '{keywords}'. Try different keywords."

    return f"Found {len(results)} review(s) mentioning '{keywords}':\n" + "\n".join(results[:limit])


def get_recommendations_for(title):
    """Returns what MDL users recommended alongside this drama, with their reasoning."""
    _load_data()
    d = _find_drama(title)
    if not d:
        return f"Drama '{title}' not found."
    recs = d.get("recommendations") or []
    if not recs:
        return f"No recommendation data for '{title}'."

    lines = [f"MDL recommendations for {d.get('title')} ({len(recs)} total):"]
    for r in recs:
        lines.append(f"  - {r.get('title', '?')} — {r.get('url', '')}")
    return "\n".join(lines)


TOOL_REGISTRY = {
    "list_dramas": lambda **kw: list_dramas(**kw),
    "search_dramas": lambda **kw: search_dramas(**kw),
    "get_drama_details": lambda **kw: get_drama_details(**kw),
    "get_drama_reviews": lambda **kw: get_drama_reviews(**kw),
    "search_reviews": lambda **kw: search_reviews(**kw),
    "get_recommendations_for": lambda **kw: get_recommendations_for(**kw),
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_dramas",
            "description": "Returns a paginated list of dramas in the database. 20 per page. Use to browse what's available without loading everything at once.",
            "parameters": {
                "type": "object",
                "properties": {
                    "page": {"type": "integer", "description": "Page number (default 1)"},
                    "per_page": {"type": "integer", "description": "Items per page (default 20)"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_dramas",
            "description": "Powerful combined search. ALL filters are AND-combined. Use to find dramas matching multiple criteria at once. For example: genre=Thriller + tag=Time Loop + keywords_in_reviews=police.",
            "parameters": {
                "type": "object",
                "properties": {
                    "genres": {"type": "string", "description": "Comma-separated genres to match (e.g. 'Thriller, Romance')"},
                    "tags": {"type": "string", "description": "Comma-separated tags to match (e.g. 'Time Loop, Investigation')"},
                    "related_to": {"type": "string", "description": "Only return dramas recommended alongside this title"},
                    "keywords_in_reviews": {"type": "string", "description": "Only return dramas whose reviews mention these keywords (e.g. 'competent police, smart detective')"},
                    "exclude": {"type": "string", "description": "Comma-separated titles to exclude from results"},
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_drama_details",
            "description": "Returns full details (synopsis, cast, genres, tags, episodes, etc) for one or MORE dramas at once. Comma-separate titles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titles": {"type": "string", "description": "One or more drama titles, comma-separated (e.g. 'Reset, Lovely Runner, Someday or One Day')"},
                },
                "required": ["titles"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_drama_reviews",
            "description": "Returns reviews for one or MORE dramas. Optionally filter reviews by keywords. Comma-separate titles.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titles": {"type": "string", "description": "One or more drama titles, comma-separated"},
                    "limit": {"type": "integer", "description": "Max reviews per drama (default 3)"},
                    "keywords": {"type": "string", "description": "Only show reviews mentioning these keywords (e.g. 'romance, chemistry')"},
                },
                "required": ["titles"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_reviews",
            "description": "Searches ALL reviews across ALL dramas for keywords. Essential for subjective queries like 'competent police', 'child protagonist', 'strong female lead'. Returns drama name + matching snippets.",
            "parameters": {
                "type": "object",
                "properties": {
                    "keywords": {"type": "string", "description": "Keywords to search, comma-separated"},
                    "limit": {"type": "integer", "description": "Max results (default 8)"},
                },
                "required": ["keywords"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recommendations_for",
            "description": "Returns dramas that MDL users recommended alongside a given title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Drama title"},
                },
                "required": ["title"],
            },
        },
    },
]
