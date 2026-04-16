from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List
from assistant_app.skills.registry import SkillExecutionContext, SkillRunResult


def _safe_session_name(session_key: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "-", session_key).strip("-")
    return cleaned or "main"


def _extract_first_url(text: str) -> str | None:
    match = re.search(r"https?://\S+", text)
    return match.group(0).rstrip(").,]}>") if match else None


def _trim_text(text: str, limit: int) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n... [truncated]"


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def _parse_json_object(text: str) -> Dict[str, Any] | None:
    text = text.strip()
    if not text:
        return None
    candidates = [text]
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if match:
        candidates.insert(0, match.group(0))
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


@dataclass
class ParsedSkillGoal:
    op: str
    url: str = ""
    host: str = ""
    query: str = ""
    start: int = 0
    end: int = 0
    limit: int = 200


class _SearxResultParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: List[Dict[str, str]] = []
        self._in_article = False
        self._current: Dict[str, str] | None = None
        self._capture_title = False
        self._title_parts: List[str] = []
        self._capture_content = False
        self._content_parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        attr_map = {key: value or "" for key, value in attrs}
        classes = attr_map.get("class", "")
        if tag == "article" and "result" in classes.split():
            self._in_article = True
            self._current = {"url": "", "title": "", "content": "", "host": ""}
            self._title_parts = []
            self._content_parts = []
            return
        if not self._in_article or self._current is None:
            return
        if tag == "a" and "url_header" in classes.split() and not self._current.get("url"):
            href = attr_map.get("href", "").strip()
            self._current["url"] = href
            try:
                self._current["host"] = urllib.parse.urlparse(href).netloc
            except Exception:
                self._current["host"] = ""
        elif tag == "h3":
            self._capture_title = True
        elif tag == "p" and "content" in classes.split():
            self._capture_content = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "article" and self._in_article:
            if self._current is not None and self._current.get("url"):
                self._current["title"] = unescape("".join(self._title_parts)).strip()
                self._current["content"] = unescape("".join(self._content_parts)).strip()
                self.results.append(self._current)
            self._in_article = False
            self._current = None
            self._capture_title = False
            self._capture_content = False
            self._title_parts = []
            self._content_parts = []
            return
        if tag == "h3":
            self._capture_title = False
        elif tag == "p":
            self._capture_content = False

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self._title_parts.append(data)
        if self._capture_content:
            self._content_parts.append(data)


class _FallbackContentParser(HTMLParser):
    _BLOCK_TAGS = {
        "article",
        "aside",
        "blockquote",
        "dd",
        "div",
        "dl",
        "dt",
        "figcaption",
        "figure",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "section",
        "table",
        "tbody",
        "td",
        "th",
        "tr",
        "ul",
    }
    _IGNORE_TAGS = {"script", "style", "noscript", "template", "svg"}

    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.title = ""
        self.blocks: List[Dict[str, Any]] = []
        self.all_links: List[Dict[str, str]] = []
        self._ignored_depth = 0
        self._title_depth = 0
        self._title_parts: List[str] = []
        self._current_tag = "body"
        self._text_parts: List[str] = []
        self._block_links: List[Dict[str, str]] = []
        self._anchor: Dict[str, Any] | None = None

    def _append_link(self, text: str, href: str, host: str) -> None:
        href = href.strip()
        if not href:
            return
        link = {
            "text": _normalize_text(text),
            "href": href,
            "host": host.strip(),
        }
        self._block_links.append(link)
        self.all_links.append(link)

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        if tag in self._IGNORE_TAGS:
            self._ignored_depth += 1
            return
        if self._ignored_depth:
            return
        if tag == "title":
            self._title_depth += 1
            return
        if tag in self._BLOCK_TAGS:
            self._flush_block()
            self._current_tag = tag
        attr_map = {key: value or "" for key, value in attrs}
        if tag in {"iframe", "video", "source"}:
            src = attr_map.get("src", "").strip() or attr_map.get("data-src", "").strip()
            resolved = urllib.parse.urljoin(self.base_url, src) if src else ""
            host = ""
            if resolved:
                try:
                    host = urllib.parse.urlparse(resolved).netloc
                except Exception:
                    host = ""
            label_parts = [
                tag,
                attr_map.get("title", ""),
                attr_map.get("aria-label", ""),
                attr_map.get("id", ""),
                attr_map.get("class", ""),
                attr_map.get("type", ""),
            ]
            self._append_link(" ".join(part for part in label_parts if part), resolved, host)
        if tag == "a":
            href = attr_map.get("href", "").strip()
            resolved = urllib.parse.urljoin(self.base_url, href) if href else ""
            host = ""
            if resolved:
                try:
                    host = urllib.parse.urlparse(resolved).netloc
                except Exception:
                    host = ""
            self._anchor = {"href": resolved, "host": host, "text_parts": []}

    def handle_endtag(self, tag: str) -> None:
        if tag in self._IGNORE_TAGS:
            if self._ignored_depth:
                self._ignored_depth -= 1
            return
        if self._ignored_depth:
            return
        if tag == "title":
            if self._title_depth:
                self._title_depth -= 1
            if not self._title_depth:
                self.title = _normalize_text("".join(self._title_parts))
                self._title_parts = []
            return
        if tag == "a" and self._anchor is not None:
            text = _normalize_text("".join(self._anchor.get("text_parts") or []))
            href = str(self._anchor.get("href", "")).strip()
            if href:
                self._append_link(text, href, str(self._anchor.get("host", "")))
            self._anchor = None
        if tag in self._BLOCK_TAGS:
            self._flush_block()

    def handle_data(self, data: str) -> None:
        if self._ignored_depth:
            return
        if self._title_depth:
            self._title_parts.append(data)
            return
        if self._anchor is not None:
            self._anchor["text_parts"].append(data)
        self._text_parts.append(data)

    def close(self) -> None:
        super().close()
        self._flush_block()
        seen = set()
        deduped_links: List[Dict[str, str]] = []
        for link in self.all_links:
            href = link.get("href", "")
            if not href or href in seen:
                continue
            seen.add(href)
            deduped_links.append(link)
        self.all_links = deduped_links

    def _flush_block(self) -> None:
        text = _normalize_text(" ".join(self._text_parts))
        unique_links: List[Dict[str, str]] = []
        seen = set()
        for link in self._block_links:
            href = link.get("href", "")
            if not href or href in seen:
                continue
            seen.add(href)
            unique_links.append(link)
        if text or unique_links:
            self.blocks.append(
                {
                    "tag": self._current_tag,
                    "text": text,
                    "links": unique_links,
                }
            )
        self._text_parts = []
        self._block_links = []


class PlaywrightCliSkill:
    def __init__(
        self,
        artifacts_dir: Path,
        workspace_root: Path,
        provider=None,
        debug_log=None,
    ) -> None:
        self.artifacts_dir = artifacts_dir
        self.workspace_root = workspace_root
        self.debug_log = debug_log

    def describe_operations(self) -> List[Dict[str, Any]]:
        return [
            {
                "op": "search",
                "description": "Consulta o motor de busca configurado e adiciona ao fluxo um artefato de links e conteúdo resumido dos resultados.",
                "params": '{"query":"Reset cdrama fansub brasileira","limit":10}',
                "precondition": "Nenhuma. Use para descobrir links antes de abrir páginas.",
            },
            {
                "op": "navigate",
                "description": "Abre uma URL e adiciona ao fluxo um artefato de links e conteúdo extraído da página.",
                "params": '{"url":"https://..."}',
                "precondition": "Nenhuma. Use para abrir páginas específicas a partir do pedido do usuário ou de links já encontrados.",
            },
            {
                "op": "filter_links",
                "description": "Filtra links do artefato atual de links e conteúdo por host e/ou trecho.",
                "params": '{"host":"drive.google.com","query":"","limit":200}',
                "precondition": "Exige artefato de links e conteúdo já criado por search ou navigate neste turno.",
            },
            {
                "op": "search_artifact",
                "description": "Busca texto ou links dentro do artefato atual de links e conteúdo.",
                "params": '{"query":"reset"}',
                "precondition": "Exige artefato de links e conteúdo já criado por search ou navigate neste turno.",
            },
            {
                "op": "get_chunks",
                "description": "Expande uma faixa de chunks do artefato atual de links e conteúdo.",
                "params": '{"start":0,"end":2}',
                "precondition": "Exige artefato de links e conteúdo já criado por search ou navigate neste turno.",
            },
            {
                "op": "list_hosts",
                "description": "Lista os hosts presentes no artefato atual de links e conteúdo.",
                "params": "{}",
                "precondition": "Exige artefato de links e conteúdo já criado por search ou navigate neste turno.",
            },
            {
                "op": "page_state",
                "description": "Mostra o estado resumido da página atual do turno.",
                "params": "{}",
                "precondition": "Exige página já aberta por navigate neste turno.",
            },
        ]

    def __call__(self, context: SkillExecutionContext) -> SkillRunResult:
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        scope_key = context.turn_id or context.session_key
        session_name = f"assistant-{_safe_session_name(scope_key)}"
        metadata = context.metadata if isinstance(context.metadata, dict) else {}
        params = metadata.get("params") if isinstance(metadata.get("params"), dict) else {}
        op = str(metadata.get("op", "")).strip()
        if op:
            goal = ParsedSkillGoal(
                op=op,
                url=str(params.get("url", "")).strip(),
                host=str(params.get("host", "")).strip(),
                query=str(params.get("query", "")).strip(),
                start=int(params.get("start", 0) or 0),
                end=int(params.get("end", 0) or 0),
                limit=int(params.get("limit", 200) or 200),
            )
        else:
            goal = self._parse_goal(context.goal, context.user_message)

        if goal.op == "search":
            result = self._search_web(scope_key, session_name, context, goal)
        elif goal.op == "navigate":
            result = self._open_and_extract(scope_key, session_name, context, goal)
        elif goal.op == "filter_links":
            result = self._filter_links(scope_key, session_name, context, goal)
        elif goal.op == "search_artifact":
            result = self._search_artifact(scope_key, session_name, context, goal)
        elif goal.op == "get_chunks":
            result = self._get_chunks(scope_key, session_name, context, goal)
        elif goal.op == "list_hosts":
            result = self._list_hosts(scope_key, session_name, context, goal)
        elif goal.op == "page_state":
            result = self._page_state_view(scope_key, session_name, context, goal)
        else:
            raise RuntimeError(f"Operação de skill não suportada: {goal.op}")

        payload = {
            "requested_goal": context.goal,
            "resolved_operation": goal.op,
            **result,
        }
        summary = self._build_summary(payload)
        return SkillRunResult(
            skill_id="playwright-browser",
            goal=context.goal,
            summary=summary,
            payload=payload,
        )

    def _parse_goal(self, goal_text: str, user_message: str) -> ParsedSkillGoal:
        structured = _parse_json_object(goal_text)
        if structured and structured.get("op"):
            op = str(structured.get("op", "")).strip()
            if op == "open_and_extract":
                op = "navigate"
            return ParsedSkillGoal(
                op=op,
                url=str(structured.get("url", "")).strip(),
                host=str(structured.get("host", "")).strip(),
                query=str(structured.get("query", "")).strip(),
                start=int(structured.get("start", 0) or 0),
                end=int(structured.get("end", 0) or 0),
                limit=int(structured.get("limit", 200) or 200),
            )

        goal_lower = goal_text.lower()
        user_lower = user_message.lower()
        combined = f"{goal_lower}\n{user_lower}"
        goal_url = _extract_first_url(goal_text) or ""
        fallback_url = _extract_first_url(user_message) or ""
        url = goal_url or fallback_url

        range_match = re.search(r"(\d+)\s*[:\-]\s*(\d+)", combined)
        if "chunk" in goal_lower or "trecho" in goal_lower or "faixa" in goal_lower:
            if range_match:
                return ParsedSkillGoal(
                    op="get_chunks",
                    start=int(range_match.group(1)),
                    end=int(range_match.group(2)),
                )

        if "buscar" in goal_lower or "pesquisar" in goal_lower or "search" in goal_lower:
            query = goal_text.strip() or user_message.strip()
            if " por " in f" {goal_lower} ":
                query = goal_text.split("por", 1)[1].strip() or query
            return ParsedSkillGoal(op="search", query=query)

        if (
            ("abrir" in goal_lower or "acessar" in goal_lower or "consultar" in goal_lower)
            and ("página" in goal_lower or "pagina" in goal_lower or goal_url or fallback_url)
        ):
            if url:
                return ParsedSkillGoal(op="navigate", url=url)

        if "host" in goal_lower or "provedor" in goal_lower or "google drive" in goal_lower or "drive.google.com" in goal_lower:
            host = ""
            if "drive.google.com" in goal_lower or "google drive" in goal_lower:
                host = "drive.google.com"
            elif "mega.nz" in goal_lower or "mega" in goal_lower:
                host = "mega.nz"
            elif "pixeldrain" in goal_lower:
                host = "pixeldrain.com"
            elif "mediafire" in goal_lower:
                host = "www.mediafire.com"
            if host:
                return ParsedSkillGoal(op="filter_links", host=host)

        if "host" in goal_lower or "domínio" in goal_lower or "dominio" in goal_lower:
            return ParsedSkillGoal(op="list_hosts")

        if "estado da página" in goal_lower or "estado da pagina" in goal_lower:
            return ParsedSkillGoal(op="page_state")

        if url:
            return ParsedSkillGoal(op="navigate", url=url)

        return ParsedSkillGoal(op="page_state")

    def _resolve_command(self) -> List[str]:
        if shutil.which("playwright-cli"):
            return ["playwright-cli"]
        return ["npx", "-y", "@playwright/cli@latest"]

    def _run(self, session_name: str, args: List[str]) -> str:
        command = self._resolve_command() + args
        env = os.environ.copy()
        env["PLAYWRIGHT_CLI_SESSION"] = session_name
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            env=env,
            cwd=self.workspace_root,
            timeout=120,
            check=False,
        )
        if completed.returncode != 0:
            stderr = (completed.stderr or completed.stdout or "").strip()
            raise RuntimeError(stderr or f"playwright-cli falhou: {' '.join(command)}")
        return completed.stdout.strip()

    def _state_path(self, scope_key: str) -> Path:
        return self.artifacts_dir / f"{_safe_session_name(scope_key)}-state.json"

    def _load_state(self, scope_key: str) -> Dict[str, Any]:
        path = self._state_path(scope_key)
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _save_state(self, scope_key: str, payload: Dict[str, Any]) -> None:
        path = self._state_path(scope_key)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _search_base_url(self) -> str:
        return os.getenv("BROWSER_SEARCH_BASE_URL", "http://127.0.0.1:8888").rstrip("/")

    def _search_fetch_results(self, query: str) -> List[Dict[str, str]]:
        base_url = self._search_base_url()
        url = f"{base_url}/search?{urllib.parse.urlencode({'q': query})}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            html = response.read().decode("utf-8", "replace")
        parser = _SearxResultParser()
        parser.feed(html)
        return parser.results

    def _page_state(self, session_name: str) -> Dict[str, Any]:
        raw = self._run(
            session_name,
            [
                "--raw",
                "eval",
                (
                    "JSON.stringify({"
                    "title: document.title,"
                    "url: location.href,"
                    "textSample: (document.body.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 5000)"
                    "})"
                ),
            ],
        )
        parsed = self._parse_eval_output(raw)
        if isinstance(parsed, dict):
            return parsed
        return {"title": "", "url": "", "textSample": str(parsed)[:5000]}

    def _parse_eval_output(self, raw_output: str) -> Any:
        raw_output = raw_output.strip()
        if not raw_output:
            return ""
        try:
            parsed = json.loads(raw_output)
        except json.JSONDecodeError:
            return raw_output
        if isinstance(parsed, str):
            try:
                reparsed = json.loads(parsed)
            except json.JSONDecodeError:
                return parsed
            return reparsed
        return parsed

    def _ensure_browser(self, session_name: str, url: str = "") -> Dict[str, Any]:
        try:
            page_state = self._page_state(session_name)
            if url and page_state.get("url") != url:
                self._run(session_name, ["goto", url])
                page_state = self._page_state(session_name)
            return page_state
        except Exception:
            if not url:
                raise
            self._run(session_name, ["open", url])
            return self._page_state(session_name)

    def _capture_snapshot(self, scope_key: str, session_name: str, label: str) -> Dict[str, Any]:
        snapshot_path = self.artifacts_dir / (
            f"{_safe_session_name(scope_key)}-{label}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.yaml"
        )
        snapshot_output = self._run(session_name, ["snapshot", f"--filename={snapshot_path}"])
        snapshot_text = snapshot_path.read_text(encoding="utf-8") if snapshot_path.exists() else ""
        return {
            "snapshot_path": str(snapshot_path),
            "snapshot_output": _trim_text(snapshot_output, 2500),
            "snapshot_preview": _trim_text(snapshot_text, 3000),
        }

    def _extract_content_artifact(self, session_name: str, scope_key: str, label: str) -> Dict[str, Any]:
        raw = self._run(session_name, ["--raw", "eval", self._artifact_eval_script()])
        parsed = self._parse_eval_output(raw)
        if not isinstance(parsed, dict):
            parsed = {"container": {}, "counts": {}, "host_counts": {}, "chunks": [], "sample_chunks": [], "all_links": []}
        artifact_path = self.artifacts_dir / (
            f"{_safe_session_name(scope_key)}-{label}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-artifact.json"
        )
        artifact = {
            "artifact_path": str(artifact_path),
            "container": parsed.get("container") or {},
            "counts": parsed.get("counts") or {},
            "host_counts": parsed.get("host_counts") or {},
            "sample_chunks": parsed.get("sample_chunks") or [],
            "chunks": parsed.get("chunks") or [],
            "all_links": parsed.get("all_links") or [],
        }
        artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
        return artifact

    def _chunks_from_blocks(self, blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunks = []
        current = {
            "id": 0,
            "start_block": 0,
            "end_block": -1,
            "char_count": 0,
            "text": "",
            "links": [],
            "hosts": {},
        }

        def flush() -> None:
            if not current["text"] and not current["links"]:
                return
            chunks.append(
                {
                    "id": current["id"],
                    "start_block": current["start_block"],
                    "end_block": current["end_block"],
                    "char_count": current["char_count"],
                    "preview": current["text"][:360],
                    "links": current["links"][:120],
                    "hosts": current["hosts"],
                }
            )

        for index, block in enumerate(blocks):
            text = str(block.get("text", "") or "")
            projected = current["char_count"] + len(text)
            if (current["text"] or current["links"]) and projected > 1400:
                flush()
                current = {
                    "id": len(chunks),
                    "start_block": index,
                    "end_block": -1,
                    "char_count": 0,
                    "text": "",
                    "links": [],
                    "hosts": {},
                }
            if not current["text"] and not current["links"]:
                current["start_block"] = index
            current["end_block"] = index
            current["char_count"] += len(text)
            if text:
                current["text"] += (" " if current["text"] else "") + text
            for link in block.get("links") or []:
                current["links"].append(link)
                host = str(link.get("host", "") or "")
                if host:
                    current["hosts"][host] = current["hosts"].get(host, 0) + 1
        flush()
        return chunks

    def _fetch_http_artifact(self, scope_key: str, label: str, url: str) -> Dict[str, Any]:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8", "replace")
            final_url = response.geturl()
        parser = _FallbackContentParser(final_url)
        parser.feed(html)
        parser.close()

        host_counts: Dict[str, int] = {}
        for link in parser.all_links:
            host = str(link.get("host", "") or "")
            if host:
                host_counts[host] = host_counts.get(host, 0) + 1
        chunks = self._chunks_from_blocks(parser.blocks)
        artifact_path = self.artifacts_dir / (
            f"{_safe_session_name(scope_key)}-{label}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-artifact.json"
        )
        artifact = {
            "artifact_path": str(artifact_path),
            "container": {"source": "http-fallback", "tag": "body", "className": "", "score": len(parser.blocks)},
            "counts": {
                "blocks": len(parser.blocks),
                "chunks": len(chunks),
                "links": len(parser.all_links),
                "text_chars": sum(len(str(block.get("text", "") or "")) for block in parser.blocks),
            },
            "host_counts": host_counts,
            "sample_chunks": chunks[:4],
            "chunks": chunks,
            "all_links": parser.all_links,
        }
        artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
        return {
            "page_state": {
                "title": parser.title,
                "url": final_url,
                "textSample": _trim_text(" ".join(str(block.get("text", "") or "") for block in parser.blocks[:12]), 5000),
            },
            "artifact": artifact,
            "fallback": {
                "used": True,
                "mode": "http",
                "source_url": url,
                "final_url": final_url,
            },
        }

    def _should_use_http_fallback(self, page_state: Dict[str, Any], artifact: Dict[str, Any], requested_url: str) -> bool:
        current_url = str(page_state.get("url", "") or "").strip()
        counts = artifact.get("counts") or {}
        empty_artifact = (
            int(counts.get("links", 0) or 0) == 0
            and int(counts.get("chunks", 0) or 0) == 0
            and int(counts.get("text_chars", 0) or 0) == 0
        )
        if current_url == "about:blank":
            return True
        if requested_url and not current_url:
            return True
        if requested_url and empty_artifact:
            return True
        return False

    def _artifact_eval_script(self) -> str:
        return (
            "JSON.stringify((() => {"
            "const normalize = (value) => (value || '').replace(/\\s+/g, ' ').trim();"
            "const resolveHost = (value) => { try { return new URL(value, location.href).host; } catch (error) { return ''; } };"
            "const buildMediaLink = (node, attrName) => {"
            "  const raw = (node.getAttribute(attrName) || '').trim();"
            "  if (!raw) return null;"
            "  const href = new URL(raw, location.href).href;"
            "  const parts = [node.tagName.toLowerCase(), node.getAttribute('title') || '', node.getAttribute('aria-label') || '', node.id || '', node.className || '', node.getAttribute('type') || ''];"
            "  return { text: normalize(parts.join(' ')), href, host: resolveHost(href) };"
            "};"
            "const dedupeLinks = (links) => links.filter((item, index, arr) => item && item.href && arr.findIndex(other => other && other.href === item.href) === index);"
            "const seen = new Set();"
            "const candidates = [];"
            "const addCandidate = (el, source) => { if (!el || seen.has(el)) return; seen.add(el); candidates.push({ el, source }); };"
            "['.post-content','.entry-content','.article-content','.article-body','.post-body','main','article','[role=main]','.content','.entry','.post'].forEach(sel => addCandidate(document.querySelector(sel), sel));"
            "addCandidate(document.body, 'body');"
            "const scoreCandidate = (item) => {"
            "  const el = item.el;"
            "  const text = normalize(el.innerText);"
            "  const paragraphs = el.querySelectorAll('p').length;"
            "  const headings = el.querySelectorAll('h1,h2,h3,h4,h5,h6').length;"
            "  const links = el.querySelectorAll('a').length;"
            "  const navish = el.querySelectorAll('nav,header,footer,aside,form').length;"
            "  const className = (el.className || '').toString().toLowerCase();"
            "  let bonus = 0;"
            "  if (item.source !== 'body') bonus += 1400;"
            "  if (/post|entry|article|content|main/.test(className)) bonus += 2600;"
            "  const textScore = Math.min(text.length, 9000);"
            "  const densityPenalty = Math.max(0, links - (paragraphs * 5) - (headings * 2)) * 25;"
            "  return bonus + textScore + (paragraphs * 260) + (headings * 140) - (navish * 450) - densityPenalty;"
            "};"
            "const best = candidates.map(item => ({ ...item, score: scoreCandidate(item) })).sort((a, b) => b.score - a.score)[0] || { el: document.body, source: 'body', score: 0 };"
            "const root = best.el || document.body;"
            "const blockSelector = 'h1,h2,h3,h4,h5,h6,p,li,blockquote,pre,table tr';"
            "let nodes = Array.from(root.querySelectorAll(blockSelector));"
            "if (!nodes.length) nodes = Array.from(root.children);"
            "const blocks = [];"
            "for (const node of nodes) {"
            "  const text = normalize(node.innerText);"
            "  if (!text) continue;"
            "  const anchorLinks = Array.from(node.querySelectorAll('a')).map((a) => {"
            "    let href = a.href || '';"
            "    return { text: normalize(a.textContent), href, host: resolveHost(href) };"
            "  });"
            "  const mediaLinks = Array.from(node.querySelectorAll('iframe,video,source')).map((el) => buildMediaLink(el, el.hasAttribute('src') ? 'src' : 'data-src'));"
            "  const links = dedupeLinks(anchorLinks.concat(mediaLinks));"
            "  blocks.push({ tag: node.tagName.toLowerCase(), text, links });"
            "}"
            "const chunks = [];"
            "let current = { id: 0, start_block: 0, end_block: -1, char_count: 0, text: '', links: [], hosts: {} };"
            "const flush = () => {"
            "  if (!current.text) return;"
            "  chunks.push({"
            "    id: current.id,"
            "    start_block: current.start_block,"
            "    end_block: current.end_block,"
            "    char_count: current.char_count,"
            "    preview: current.text.slice(0, 360),"
            "    links: current.links.slice(0, 120),"
            "    hosts: current.hosts"
            "  });"
            "};"
            "blocks.forEach((block, index) => {"
            "  const projected = current.char_count + block.text.length;"
            "  if (current.text && projected > 1400) { flush(); current = { id: chunks.length, start_block: index, end_block: -1, char_count: 0, text: '', links: [], hosts: {} }; }"
            "  if (!current.text) current.start_block = index;"
            "  current.end_block = index;"
            "  current.char_count += block.text.length;"
            "  current.text += (current.text ? ' ' : '') + block.text;"
            "  for (const link of block.links) {"
            "    current.links.push(link);"
            "    if (link.host) current.hosts[link.host] = (current.hosts[link.host] || 0) + 1;"
            "  }"
            "});"
            "flush();"
            "const anchorLinks = Array.from(root.querySelectorAll('a')).map((a) => {"
            "  let href = a.href || '';"
            "  return { text: normalize(a.textContent), href, host: resolveHost(href) };"
            "});"
            "const mediaLinks = Array.from(root.querySelectorAll('iframe,video,source')).map((el) => buildMediaLink(el, el.hasAttribute('src') ? 'src' : 'data-src'));"
            "const allLinks = dedupeLinks(anchorLinks.concat(mediaLinks));"
            "const hostCounts = {};"
            "for (const link of allLinks) { const host = link.host || ''; hostCounts[host] = (hostCounts[host] || 0) + 1; }"
            "return {"
            "  container: { source: best.source || 'body', tag: (root.tagName || '').toLowerCase(), className: root.className || '', score: best.score || 0 },"
            "  counts: { blocks: blocks.length, chunks: chunks.length, links: allLinks.length, text_chars: normalize(root.innerText).length },"
            "  host_counts: hostCounts,"
            "  sample_chunks: chunks.slice(0, 4),"
            "  chunks,"
            "  all_links: allLinks"
            "};"
            "})())"
        )

    def _available_tools(self, artifact: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {"op": "search", "description": "Consulta o motor de busca configurado e adiciona um novo artefato de links e conteúdo ao fluxo.", "parameters": {"query": "<busca>", "limit": 10}},
            {"op": "list_hosts", "description": "Lista os hosts e as quantidades de links do artefato atual de links e conteúdo."},
            {"op": "filter_links", "description": "Filtra links do artefato atual por host ou trecho.", "parameters": {"host": "<host>", "query": "<trecho opcional>", "limit": 200}},
            {"op": "search_artifact", "description": "Busca texto ou links dentro dos chunks do artefato atual.", "parameters": {"query": "<texto>"}},
            {"op": "get_chunks", "description": "Expande uma faixa de chunks do artefato atual.", "parameters": {"start": 0, "end": 2}},
            {"op": "page_state", "description": "Mostra o estado atual da página e o snapshot resumido."},
        ]

    def _missing_from_current_view(self, artifact: Dict[str, Any], current_view: Dict[str, Any]) -> List[str]:
        counts = artifact.get("counts") or {}
        current_kind = current_view.get("kind", "")
        missing = []
        if current_kind != "host_counts":
            missing.append("host_counts_completos")
        if current_kind != "filtered_links":
            missing.append("lista_completa_de_links_filtrados")
        if current_kind != "chunk_range":
            missing.append(f"chunks_restantes_ate_{counts.get('chunks', 0)}")
        if current_kind != "search_results":
            missing.append("busca_por_termo_no_artefato")
        return missing

    def _load_artifact(self, scope_key: str) -> Dict[str, Any]:
        state = self._load_state(scope_key)
        artifact_path = state.get("artifact_path")
        if not artifact_path:
            raise RuntimeError("Nenhum artefato atual de links e conteúdo salvo para esta sessão.")
        path = Path(str(artifact_path))
        if not path.exists():
            raise RuntimeError(f"Artefato atual de links e conteúdo não encontrado: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def _write_cycle_log(self, payload: Dict[str, Any]) -> None:
        if self.debug_log is None:
            return
        try:
            self.debug_log.write("skill_cycle", payload)
        except Exception:
            return

    def _open_and_extract(self, scope_key: str, session_name: str, context: SkillExecutionContext, goal: ParsedSkillGoal) -> Dict[str, Any]:
        page_state = self._ensure_browser(session_name, goal.url)
        snapshot = self._capture_snapshot(scope_key, session_name, "open")
        artifact = self._extract_content_artifact(session_name, scope_key, "open")
        fallback = {"used": False, "mode": "", "source_url": "", "final_url": ""}
        if goal.url and self._should_use_http_fallback(page_state, artifact, goal.url):
            fallback_result = self._fetch_http_artifact(scope_key, "http-open", goal.url)
            page_state = fallback_result["page_state"]
            artifact = fallback_result["artifact"]
            fallback = fallback_result["fallback"]
        state = {
            "current_url": page_state.get("url", ""),
            "artifact_path": artifact.get("artifact_path", ""),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save_state(scope_key, state)
        current_view = {
            "kind": "sample_chunks",
            "coverage": "sample",
            "returned_chunks": len(artifact.get("sample_chunks") or []),
            "total_chunks": int((artifact.get("counts") or {}).get("chunks", 0) or 0),
        }
        self._write_cycle_log(
            {
                "turn_id": context.turn_id,
                "session_key": context.session_key,
                "skill_id": "playwright-browser",
                "op": "navigate",
                "url": goal.url,
                "page_state": {
                    "title": page_state.get("title", ""),
                    "url": page_state.get("url", ""),
                },
                "fallback": fallback,
                "artifact_summary": {
                    "container": artifact.get("container", {}),
                    "counts": artifact.get("counts", {}),
                    "host_counts": artifact.get("host_counts", {}),
                },
            }
        )
        return {
            "session_name": session_name,
            "page_state": {
                "title": page_state.get("title", ""),
                "url": page_state.get("url", ""),
                "text_sample": _trim_text(str(page_state.get("textSample", "")), 2000),
            },
            "fallback": fallback,
            "snapshot": snapshot,
            "content_artifact_summary": {
                "artifact_path": artifact.get("artifact_path", ""),
                "artifact_kind": "page_links_and_content_http_fallback" if fallback.get("used") else "page_links_and_content",
                "container": artifact.get("container", {}),
                "counts": artifact.get("counts", {}),
                "host_counts": artifact.get("host_counts", {}),
                "sample_chunks": artifact.get("sample_chunks", []),
            },
            "current_view": current_view,
            "available_tools": self._available_tools(artifact),
            "missing_from_current_view": self._missing_from_current_view(artifact, current_view),
        }

    def _search_web(self, scope_key: str, session_name: str, context: SkillExecutionContext, goal: ParsedSkillGoal) -> Dict[str, Any]:
        query = goal.query.strip() or context.user_message.strip()
        limit = max(1, min(goal.limit or 10, 50))
        results = self._search_fetch_results(query)[:limit]
        artifact_path = self.artifacts_dir / (
            f"{_safe_session_name(scope_key)}-search-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-artifact.json"
        )
        chunks = []
        all_links = []
        host_counts: Dict[str, int] = {}
        for index, item in enumerate(results):
            link = {
                "text": item.get("title", ""),
                "href": item.get("url", ""),
                "host": item.get("host", ""),
            }
            all_links.append(link)
            if link["host"]:
                host_counts[link["host"]] = host_counts.get(link["host"], 0) + 1
            chunks.append(
                {
                    "id": index,
                    "start_block": index,
                    "end_block": index,
                    "char_count": len(item.get("content", "")),
                    "preview": item.get("content", "")[:360],
                    "links": [link],
                    "hosts": {link["host"]: 1} if link["host"] else {},
                }
            )
        artifact = {
            "artifact_path": str(artifact_path),
            "container": {"source": "search", "tag": "search-results", "className": "search-results", "score": len(results)},
            "counts": {"blocks": len(results), "chunks": len(chunks), "links": len(all_links), "text_chars": sum(len(item.get("content", "")) for item in results)},
            "host_counts": host_counts,
            "sample_chunks": chunks[:4],
            "chunks": chunks,
            "all_links": all_links,
        }
        artifact_path.write_text(json.dumps(artifact, ensure_ascii=False, indent=2), encoding="utf-8")
        self._save_state(
            scope_key,
            {
                "current_url": f"{self._search_base_url()}/search?{urllib.parse.urlencode({'q': query})}",
                "artifact_path": str(artifact_path),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
        )
        current_view = {
            "kind": "search_results_page",
            "coverage": "complete",
            "returned_chunks": len(chunks[:4]),
            "total_chunks": len(chunks),
            "query": query,
        }
        self._write_cycle_log(
            {
                "turn_id": context.turn_id,
                "session_key": context.session_key,
                "skill_id": "playwright-browser",
                "op": "search",
                "query": query,
                "result_count": len(results),
                "search_base_url": self._search_base_url(),
            }
        )
        return {
            "session_name": session_name,
            "page_state": {
                "title": f"Resultados de busca para: {query}",
                "url": f"{self._search_base_url()}/search?{urllib.parse.urlencode({'q': query})}",
                "text_sample": _trim_text(" ".join(item.get("content", "") for item in results[:4]), 2000),
            },
            "content_artifact_summary": {
                "artifact_path": str(artifact_path),
                "artifact_kind": "search_links_and_content",
                "container": artifact.get("container", {}),
                "counts": artifact.get("counts", {}),
                "host_counts": artifact.get("host_counts", {}),
                "sample_chunks": artifact.get("sample_chunks", []),
            },
            "current_view": current_view,
            "available_tools": self._available_tools(artifact),
            "missing_from_current_view": self._missing_from_current_view(artifact, current_view),
            "result": {"results": results},
        }

    def _filter_links(self, scope_key: str, session_name: str, context: SkillExecutionContext, goal: ParsedSkillGoal) -> Dict[str, Any]:
        artifact = self._load_artifact(scope_key)
        needle_host = goal.host.lower().strip()
        needle_query = goal.query.lower().strip()
        filtered = []
        for link in artifact.get("all_links") or []:
            host = str(link.get("host", "")).lower()
            href = str(link.get("href", "")).lower()
            text = str(link.get("text", "")).lower()
            if needle_host and needle_host not in host:
                continue
            if needle_query and needle_query not in href and needle_query not in text and needle_query not in host:
                continue
            filtered.append(link)
        returned = filtered[: goal.limit]
        coverage = "complete" if len(returned) == len(filtered) else "partial"
        current_view = {
            "kind": "filtered_links",
            "coverage": coverage,
            "filter": {"host": goal.host, "query": goal.query},
            "returned_count": len(returned),
            "total_count": len(filtered),
        }
        self._write_cycle_log(
            {
                "turn_id": context.turn_id,
                "session_key": context.session_key,
                "skill_id": "playwright-browser",
                "op": "filter_links",
                "host": goal.host,
                "query": goal.query,
                "result_count": len(filtered),
                "returned_count": len(returned),
            }
        )
        return {
            "session_name": session_name,
            "filter": {"host": goal.host, "query": goal.query, "limit": goal.limit},
            "result": {"links": returned, "count": len(filtered)},
            "content_artifact_summary": {
                "artifact_path": artifact.get("artifact_path", ""),
                "artifact_kind": "links_and_content",
                "counts": artifact.get("counts", {}),
                "host_counts": artifact.get("host_counts", {}),
            },
            "current_view": current_view,
            "available_tools": self._available_tools(artifact),
            "missing_from_current_view": self._missing_from_current_view(artifact, current_view),
        }

    def _search_artifact(self, scope_key: str, session_name: str, context: SkillExecutionContext, goal: ParsedSkillGoal) -> Dict[str, Any]:
        artifact = self._load_artifact(scope_key)
        needle = goal.query.lower().strip()
        matches = []
        for chunk in artifact.get("chunks") or []:
            values = [str(chunk.get("preview", ""))]
            values.extend(str(link.get("href", "")) for link in chunk.get("links") or [])
            values.extend(str(link.get("text", "")) for link in chunk.get("links") or [])
            if any(needle in value.lower() for value in values if value):
                matches.append(
                    {
                        "chunk_id": chunk.get("id"),
                        "preview": chunk.get("preview", ""),
                        "hosts": chunk.get("hosts", {}),
                    }
                )
        current_view = {
            "kind": "search_results",
            "coverage": "complete",
            "query": goal.query,
            "returned_count": len(matches),
            "total_count": len(matches),
        }
        self._write_cycle_log(
            {
                "turn_id": context.turn_id,
                "session_key": context.session_key,
                "skill_id": "playwright-browser",
                "op": "search_artifact",
                "query": goal.query,
                "result_count": len(matches),
            }
        )
        return {
            "session_name": session_name,
            "query": goal.query,
            "result": {"matches": matches},
            "content_artifact_summary": {
                "artifact_path": artifact.get("artifact_path", ""),
                "artifact_kind": "links_and_content",
                "counts": artifact.get("counts", {}),
                "host_counts": artifact.get("host_counts", {}),
            },
            "current_view": current_view,
            "available_tools": self._available_tools(artifact),
            "missing_from_current_view": self._missing_from_current_view(artifact, current_view),
        }

    def _get_chunks(self, scope_key: str, session_name: str, context: SkillExecutionContext, goal: ParsedSkillGoal) -> Dict[str, Any]:
        artifact = self._load_artifact(scope_key)
        selected = [chunk for chunk in artifact.get("chunks") or [] if goal.start <= int(chunk.get("id", -1)) <= goal.end]
        current_view = {
            "kind": "chunk_range",
            "coverage": "complete",
            "range": {"start": goal.start, "end": goal.end},
            "returned_count": len(selected),
            "total_count": len(selected),
        }
        self._write_cycle_log(
            {
                "turn_id": context.turn_id,
                "session_key": context.session_key,
                "skill_id": "playwright-browser",
                "op": "get_chunks",
                "start": goal.start,
                "end": goal.end,
                "returned_count": len(selected),
            }
        )
        return {
            "session_name": session_name,
            "range": {"start": goal.start, "end": goal.end},
            "result": {"chunks": selected},
            "content_artifact_summary": {
                "artifact_path": artifact.get("artifact_path", ""),
                "artifact_kind": "links_and_content",
                "counts": artifact.get("counts", {}),
                "host_counts": artifact.get("host_counts", {}),
            },
            "current_view": current_view,
            "available_tools": self._available_tools(artifact),
            "missing_from_current_view": self._missing_from_current_view(artifact, current_view),
        }

    def _list_hosts(self, scope_key: str, session_name: str, context: SkillExecutionContext, goal: ParsedSkillGoal) -> Dict[str, Any]:
        artifact = self._load_artifact(scope_key)
        current_view = {
            "kind": "host_counts",
            "coverage": "complete",
            "returned_count": len(artifact.get("host_counts") or {}),
            "total_count": len(artifact.get("host_counts") or {}),
        }
        self._write_cycle_log(
            {
                "turn_id": context.turn_id,
                "session_key": context.session_key,
                "skill_id": "playwright-browser",
                "op": "list_hosts",
                "returned_count": len(artifact.get("host_counts") or {}),
            }
        )
        return {
            "session_name": session_name,
            "result": {"host_counts": artifact.get("host_counts", {})},
            "content_artifact_summary": {
                "artifact_path": artifact.get("artifact_path", ""),
                "artifact_kind": "links_and_content",
                "counts": artifact.get("counts", {}),
                "host_counts": artifact.get("host_counts", {}),
            },
            "current_view": current_view,
            "available_tools": self._available_tools(artifact),
            "missing_from_current_view": self._missing_from_current_view(artifact, current_view),
        }

    def _page_state_view(self, scope_key: str, session_name: str, context: SkillExecutionContext, goal: ParsedSkillGoal) -> Dict[str, Any]:
        state = self._load_state(scope_key)
        page_state = self._ensure_browser(session_name, state.get("current_url", ""))
        snapshot = self._capture_snapshot(scope_key, session_name, "page-state")
        self._write_cycle_log(
            {
                "turn_id": context.turn_id,
                "session_key": context.session_key,
                "skill_id": "playwright-browser",
                "op": "page_state",
                "page_state": {
                    "title": page_state.get("title", ""),
                    "url": page_state.get("url", ""),
                },
            }
        )
        return {
            "session_name": session_name,
            "page_state": {
                "title": page_state.get("title", ""),
                "url": page_state.get("url", ""),
                "text_sample": _trim_text(str(page_state.get("textSample", "")), 2000),
            },
            "snapshot": snapshot,
            "current_view": {
                "kind": "page_state",
                "coverage": "complete",
                "returned_count": 1,
                "total_count": 1,
            },
            "available_tools": [],
            "missing_from_current_view": [],
        }

    def cleanup_turn(self, turn_id: str) -> None:
        scope_key = turn_id.strip()
        if not scope_key:
            return
        session_name = f"assistant-{_safe_session_name(scope_key)}"
        try:
            self._run(session_name, ["close"])
        except Exception:
            pass
        try:
            self._state_path(scope_key).unlink(missing_ok=True)
        except Exception:
            pass

    def _build_summary(self, payload: Dict[str, Any]) -> str:
        page_state = payload.get("page_state") or {}
        artifact_summary = payload.get("content_artifact_summary") or {}
        current_view = payload.get("current_view") or {}
        fallback = payload.get("fallback") or {}
        counts = artifact_summary.get("counts") or {}
        lines = [
            f"Skill playwright-browser executada: {payload.get('resolved_operation', '')}",
            f"Página: {page_state.get('title', 'sem título')}",
            f"URL: {page_state.get('url', '')}",
            f"View atual: {current_view.get('kind', '')} ({current_view.get('coverage', '')})",
            f"Links no artefato de links e conteúdo: {counts.get('links', 0)}",
            f"Chunks no artefato de links e conteúdo: {counts.get('chunks', 0)}",
        ]
        if fallback.get("used"):
            lines.append(f"Fallback aplicado: {fallback.get('mode', '')}")
        result = payload.get("result") or {}
        if current_view.get("kind") == "filtered_links":
            lines.append(f"Links filtrados retornados: {len(result.get('links') or [])}")
            lines.append(f"Links filtrados totais: {int((result.get('count') or 0))}")
        elif payload.get("resolved_operation") == "search":
            lines.append(f"Resultados de busca retornados: {len(result.get('results') or [])}")
        return "\n".join(lines).strip()
