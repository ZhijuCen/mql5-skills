#!/usr/bin/env python3
"""
Two-phase MQL5 content extraction: download HTML → convert to Markdown.

Phase 1 (download):  Fetch all HTML from mql5.com, save losslessly to html_cache/
Phase 2 (convert):   Parse local HTML, download images, write Markdown files

Usage:
    # Phase 1: download all HTML
    python scripts/extract.py download --sitemap sitemaps/sitemap_book_en.xml
    python scripts/extract.py download --sitemap sitemaps/sitemap_docs_en.xml
    python scripts/extract.py download --all

    # Phase 2: convert HTML → Markdown
    python scripts/extract.py convert --sitemap sitemaps/sitemap_book_en.xml
    python scripts/extract.py convert --sitemap sitemaps/sitemap_docs_en.xml
    python scripts/extract.py convert --all

    # Debug single page (fetches + converts)
    python scripts/extract.py debug URL
"""

import argparse
import hashlib
import logging
import os
import random
import re
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENTS = {
    "firefox": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "msedge": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0",
    "chromium": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
}
UA_KEYS = list(USER_AGENTS.keys())
_NUM_UA = len(UA_KEYS)


def load_user_agents_csv(csv_path: str) -> None:
    """Load User-Agent strings from a CSV file, replacing module-level UA pool.

    CSV must have a ``user_agent`` column.  Each row becomes one entry;
    keys are ``u0``, ``u1``, … in file order.
    """
    global USER_AGENTS, UA_KEYS, _NUM_UA
    import csv as _csv

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = _csv.DictReader(f)
        if "user_agent" not in (reader.fieldnames or []):
            raise ValueError(f"CSV {csv_path} has no 'user_agent' column")
        pool = {f"u{i}": row["user_agent"] for i, row in enumerate(reader)}

    if not pool:
        raise ValueError(f"CSV {csv_path} contains no User-Agent rows")

    USER_AGENTS = pool
    UA_KEYS = list(USER_AGENTS.keys())
    _NUM_UA = len(UA_KEYS)
    log.info("Loaded %d User-Agents from %s", _NUM_UA, csv_path)


def get_user_agent(index: int | None = None) -> str:
    """Return a User-Agent string. Deterministic by index, or random."""
    if index is not None:
        return USER_AGENTS[UA_KEYS[index % _NUM_UA]]
    return USER_AGENTS[random.choice(UA_KEYS)]

REQUEST_DELAY = 0.9  # seconds between requests
MAX_RETRIES = 3
RETRY_BACKOFF = 2  # exponential backoff multiplier

SITEMAP_NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

# CSS selector for main content start
CONTENT_START_SELECTOR = "#help > h1:nth-child(1)"

# HTML cache root
HTML_CACHE_ROOT = Path("html_cache")

# Mapping: sitemap path → (output md dir, label)
SITEMAP_DEFAULTS = {
    "sitemaps/sitemap_book_en.xml": (
        "skills/mql5/references/book",
        "book",
    ),
    "sitemaps/sitemap_docs_en.xml": (
        "skills/mql5/references/docs",
        "docs",
    ),
}

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

log = logging.getLogger("extract")


# ---------------------------------------------------------------------------
# Sitemap parsing
# ---------------------------------------------------------------------------


def parse_sitemap(sitemap_path: str) -> list[str]:
    """Extract <loc> URLs from a sitemap XML file, in document order."""
    tree = ET.parse(sitemap_path)
    urls = [loc.text for loc in tree.findall(".//s:url/s:loc", SITEMAP_NS)]
    log.info("Parsed %d URLs from %s", len(urls), sitemap_path)
    return urls


# ---------------------------------------------------------------------------
# URL → file mapping  (naming convention, shared by both phases)
# ---------------------------------------------------------------------------


def sanitize_name(name: str) -> str:
    """Convert a URL segment to a safe file/folder name."""
    name = name.lower()
    name = name.replace("_", "-")
    name = re.sub(r"[^a-z0-9-]", "", name)
    name = re.sub(r"-{2,}", "-", name)
    name = name.strip("-")
    return name


def derive_name_from_url(url: str, root_prefix: str) -> str:
    """Given a full URL and the root prefix (e.g. '/en/book/'),
    return the 'path tail' used for naming."""
    path = url
    if path.startswith("http"):
        parsed = urlparse(path)
        path = parsed.path

    path_clean = path.strip("/")
    prefix_clean = root_prefix.strip("/")

    if path_clean.lower() == prefix_clean.lower():
        return ""
    if path_clean.lower().startswith(prefix_clean.lower() + "/"):
        return path_clean[len(prefix_clean) + 1 :]
    return path_clean


def build_file_map(
    urls: list[str], root_prefix: str, output_dir: str, label: str
) -> list[dict]:
    """Build the mapping from URL index → file path.

    Returns a list of dicts with keys:
        url, index (0-based), file_path (.md), html_path (.html),
        chapter_folder, filename
    """
    html_cache_dir = HTML_CACHE_ROOT / label
    file_map = []
    chapter_counter = 0
    chapter_map: dict[str, int] = {}

    for idx, url in enumerate(urls):
        tail = derive_name_from_url(url, root_prefix)
        parts = tail.split("/") if tail else []

        if not parts:
            # Root URL
            base = f"{idx:04d}-{label}"
            filename_md = f"{base}.md"
            filename_html = f"{base}.html"
            file_path = Path(output_dir) / filename_md
            html_path = html_cache_dir / filename_html
            chapter_folder = None
        else:
            depth1 = parts[0]
            if depth1 not in chapter_map:
                chapter_map[depth1] = chapter_counter
                chapter_counter += 1
            ch_num = chapter_map[depth1]
            chapter_folder = f"{ch_num:02d}-{sanitize_name(depth1)}"

            if len(parts) == 1:
                derived = sanitize_name(depth1)
            else:
                derived = "-".join(sanitize_name(p) for p in parts)

            base = f"{idx:04d}-{derived}"
            filename_md = f"{base}.md"
            filename_html = f"{base}.html"
            file_path = Path(output_dir) / chapter_folder / filename_md
            html_path = html_cache_dir / chapter_folder / filename_html

        file_map.append(
            {
                "url": url,
                "index": idx,
                "file_path": str(file_path),
                "html_path": str(html_path),
                "chapter_folder": chapter_folder,
                "filename": filename_md,
            }
        )

    log.info(
        "Built file map: %d files, %d chapters",
        len(file_map),
        chapter_counter,
    )
    return file_map


# ---------------------------------------------------------------------------
# Phase 1: Download HTML
# ---------------------------------------------------------------------------


def fetch_html(url: str, session: requests.Session) -> str | None:
    """Fetch a URL with retry + backoff. Returns HTML text or None on failure."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.text
            if resp.status_code in (429, 500, 502, 503, 504):
                wait = RETRY_BACKOFF**attempt
                log.warning(
                    "HTTP %d for %s, retry %d/%d in %ds",
                    resp.status_code, url, attempt, MAX_RETRIES, wait,
                )
                time.sleep(wait)
                continue
            log.error("HTTP %d for %s — skipping", resp.status_code, url)
            return None
        except requests.RequestException as exc:
            wait = RETRY_BACKOFF**attempt
            log.warning(
                "Request error for %s: %s, retry %d/%d in %ds",
                url, exc, attempt, MAX_RETRIES, wait,
            )
            time.sleep(wait)
    log.error("All %d retries failed for %s", MAX_RETRIES, url)
    return None


def download_one(url: str, html_path: str, session: requests.Session) -> bool:
    """Download a single URL and save to html_path. Returns True on success."""
    out = Path(html_path)
    if out.exists():
        log.debug("Already cached: %s", html_path)
        return True

    html = fetch_html(url, session)
    if html is None:
        return False

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return True


def run_download(
    sitemap_path: str,
    force: bool = False,
    dry_run: bool = False,
    random_ua: bool = False,
    random_delay: bool = False,
    user_agents_csv: str | None = None,
) -> None:
    """Phase 1: download all HTML files for a sitemap."""
    if user_agents_csv:
        load_user_agents_csv(user_agents_csv)
    urls = parse_sitemap(sitemap_path)
    root_prefix = _root_prefix_from_sitemap(sitemap_path)
    label = _label_from_sitemap(sitemap_path)
    md_output_dir = SITEMAP_DEFAULTS.get(sitemap_path, ("", label))[0]

    file_map = build_file_map(urls, root_prefix, md_output_dir, label)

    if dry_run:
        print(f"\n=== Download dry run: {sitemap_path} ===")
        print(f"Total URLs: {len(file_map)}")
        print(f"Cache dir: {HTML_CACHE_ROOT / label}")
        for entry in file_map[:20]:
            print(f"  [{entry['index']:4d}] {entry['url']}")
            print(f"         → {entry['html_path']}")
        if len(file_map) > 20:
            print(f"  ... ({len(file_map) - 20} more)")
        return

    # Progress log
    log_path = HTML_CACHE_ROOT / label / ".download.log"
    processed = _load_log(log_path) if not force else set()

    session = requests.Session()

    success = 0
    skipped = 0
    failed = 0

    for entry in file_map:
        url = entry["url"]
        if url in processed and not force:
            skipped += 1
            continue

        session.headers.update({
            "User-Agent": get_user_agent() if random_ua else get_user_agent(entry["index"])
        })
        ok = download_one(url, entry["html_path"], session)
        if ok:
            success += 1
            _append_log(log_path, url)
            log.info("[%d/%d] OK: %s", success + skipped + failed, len(file_map), url)
        else:
            failed += 1
            log.error("[%d/%d] FAIL: %s", success + skipped + failed, len(file_map), url)

        if random_delay:
            time.sleep(REQUEST_DELAY * random.uniform(1.0, 3.0))
        else:
            time.sleep(REQUEST_DELAY)

    log.info(
        "Done: %d success, %d skipped, %d failed (total %d)",
        success, skipped, failed, len(file_map),
    )


# ---------------------------------------------------------------------------
# Phase 2: Convert HTML → Markdown
# ---------------------------------------------------------------------------

# Image downloading (only needed during convert phase)


def download_image(
    img_url: str, pics_dir: Path, session: requests.Session
) -> str | None:
    """Download an image, save to pics_dir, return local filename or None."""
    parsed = urlparse(img_url)
    name = Path(parsed.path).name
    if not name or "." not in name:
        ext = ".png"
        name = hashlib.md5(img_url.encode()).hexdigest()[:12] + ext

    local_path = pics_dir / name
    if local_path.exists():
        return name

    try:
        resp = session.get(img_url, timeout=30)
        if resp.status_code == 200:
            local_path.parent.mkdir(parents=True, exist_ok=True)
            local_path.write_bytes(resp.content)
            return name
    except requests.RequestException as exc:
        log.warning("Failed to download image %s: %s", img_url, exc)
    return None


# HTML → Markdown conversion helpers


def get_text(el: Tag | NavigableString, sep: str = "") -> str:
    """Recursively get text content."""
    if isinstance(el, NavigableString):
        return str(el)
    parts = []
    for child in el.children:
        t = get_text(child, sep)
        if t:
            parts.append(t)
    return sep.join(parts)


def inline_to_md(el: Tag) -> str:
    """Convert an inline element to Markdown."""
    if isinstance(el, NavigableString):
        return str(el)

    tag = el.name
    inner = "".join(inline_to_md(c) for c in el.children)

    if tag in ("strong", "b"):
        return f"**{inner}**"
    if tag in ("em", "i"):
        return f"*{inner}*"
    if tag == "code":
        if "`" in inner:
            return f"`` {inner} ``"
        return f"`{inner}`"
    if tag == "a":
        href = el.get("href", "")
        if href and not href.startswith("#"):
            return f"[{inner}]({href})"
        return inner
    if tag == "br":
        return "  \n"
    if tag == "img":
        src = el.get("src", "")
        alt = el.get("alt", "")
        return f"![{alt}]({src})"
    if tag in ("span", "font", "u", "s", "sub", "sup", "small", "big", "mark"):
        return inner
    return inner


def table_to_md(table: Tag) -> str:
    """Convert a <table> to Markdown.

    Has <thead> → data table. No <thead> → code block.
    """
    thead = table.find("thead")
    tbody = table.find("tbody") or table

    if thead:
        rows = []
        for tr in thead.find_all("tr"):
            cells = [get_text(td, " ").strip() for td in tr.find_all(["th", "td"])]
            rows.append(cells)

        ncols = max((len(r) for r in rows), default=0)
        if rows and ncols:
            rows.append(["---"] * ncols)

        body_rows = tbody.find_all("tr") if tbody else []
        for tr in body_rows:
            if thead and tr.find_parent("thead"):
                continue
            cells = [get_text(td, " ").strip() for td in tr.find_all(["th", "td"])]
            rows.append(cells)

        lines = []
        for row in rows:
            while len(row) < ncols:
                row.append("")
            lines.append("| " + " | ".join(row) + " |")
        return "\n".join(lines)
    else:
        code_lines = []
        all_rows = tbody.find_all("tr") if tbody else table.find_all("tr")
        for tr in all_rows:
            cells = tr.find_all(["td", "th"])
            for cell in cells:
                code_el = cell.find("code") or cell.find("pre")
                if code_el:
                    code_lines.append(get_text(code_el, "\n"))
                else:
                    text = cell.get_text()
                    if text.strip():
                        code_lines.append(text)

        code_text = "\n".join(code_lines)
        lang = detect_code_lang(table)
        return f"```{lang}\n{code_text}\n```"


def detect_code_lang(el: Tag) -> str:
    """Try to detect code language from CSS classes."""
    classes = el.get("class", [])
    if isinstance(classes, str):
        classes = classes.split()
    for cls in classes:
        cl = cls.lower()
        if "mql" in cl or "cpp" in cl or "c-plus" in cl:
            return "cpp"
        if "console" in cl or "output" in cl or "result" in cl:
            return ""
        if "sql" in cl:
            return "sql"
    parent = el.parent
    if parent and isinstance(parent, Tag):
        return detect_code_lang(parent)
    return ""


def pre_to_md(pre: Tag) -> str:
    """Convert <pre><code> to fenced Markdown code."""
    code = pre.find("code")
    if code:
        lang = detect_code_lang(code)
        text = get_text(code, "\n")
    else:
        lang = ""
        text = get_text(pre, "\n")
    return f"```{lang}\n{text}\n```"


def element_to_md(
    el: Tag,
    pics_dir: Path | None,
    session: requests.Session | None,
    base_url: str,
    img_cache: dict[str, str | None],
) -> str:
    """Convert a single content element to Markdown string."""
    if isinstance(el, NavigableString):
        text = str(el).strip()
        return text if text else ""

    tag = el.name

    # --- Headings ---
    if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        level = int(tag[1])
        text = get_text(el, " ").strip()
        return f"{'#' * level} {text}\n"

    # --- Paragraphs ---
    if tag == "p":
        img_child = el.find("img")
        if img_child:
            return element_to_md(img_child, pics_dir, session, base_url, img_cache)
        inner = "".join(inline_to_md(c) for c in el.children)
        inner = inner.strip()
        if not inner:
            return ""
        return f"{inner}\n"

    # --- Images ---
    if tag == "img":
        src = el.get("src", "")
        if not src:
            return ""

        if src.startswith("/"):
            src = f"https://www.mql5.com{src}"
        elif not src.startswith("http"):
            src = f"{base_url.rstrip('/')}/{src}"

        # Get alt text
        alt_text = ""
        next_sibling = el.find_next_sibling("p")
        if not next_sibling and el.parent and isinstance(el.parent, Tag):
            next_sibling = el.parent.find_next_sibling("p")
        if next_sibling:
            alt_text = get_text(next_sibling, " ").strip()
        if not alt_text:
            alt_text = el.get("alt", "")

        # Download image
        img_filename = None
        if pics_dir and session:
            if src in img_cache:
                img_filename = img_cache[src]
            else:
                img_filename = download_image(src, pics_dir, session)
                img_cache[src] = img_filename

        if img_filename:
            return f"![{alt_text}](pics/{img_filename})\n"
        else:
            return f"![{alt_text}]({src})\n"

    # --- Tables ---
    if tag == "table":
        return table_to_md(el) + "\n"

    # --- Preformatted code ---
    if tag == "pre":
        return pre_to_md(el) + "\n"

    # --- Lists ---
    if tag in ("ul", "ol"):
        items = []
        for i, li in enumerate(el.find_all("li", recursive=False)):
            prefix = f"{i+1}. " if tag == "ol" else "- "
            # If <li> contains an <img>, handle it through element_to_md
            img_child = li.find("img")
            if img_child:
                img_md = element_to_md(img_child, pics_dir, session, base_url, img_cache)
                # Get remaining text after the image
                rest = "".join(inline_to_md(c) for c in li.children if not (isinstance(c, Tag) and c.name == "img"))
                inner = (img_md.strip() + " " + rest.strip()).strip()
            else:
                inner = "".join(inline_to_md(c) for c in li.children)
            items.append(f"{prefix}{inner.strip()}")
        return "\n".join(items) + "\n"

    # --- Blockquote ---
    if tag == "blockquote":
        inner = get_text(el, " ").strip()
        lines = inner.split("\n")
        return "\n".join(f"> {line}" for line in lines) + "\n"

    # --- Horizontal rule ---
    if tag == "hr":
        return "---\n"

    # --- Code (standalone) ---
    if tag == "code":
        text = get_text(el, "\n")
        return f"`{text}`\n"

    # --- Block containers: recurse ---
    if tag in ("div", "section", "article", "figure", "figcaption",
               "dl", "dd", "dt", "details", "summary", "main", "aside"):
        parts = []
        for child in el.children:
            if isinstance(child, NavigableString):
                text = str(child).strip()
                if text:
                    parts.append(text)
            elif isinstance(child, Tag):
                md = element_to_md(child, pics_dir, session, base_url, img_cache)
                if md:
                    parts.append(md)
        return "\n".join(parts)

    # --- Unknown tag ---
    inner = "".join(inline_to_md(c) for c in el.children)
    return inner.strip() if inner.strip() else ""


def extract_content(html: str, url: str) -> list[PageElement]:
    """Parse HTML and extract the main content elements from #help."""
    soup = BeautifulSoup(html, "html.parser")

    help_div = soup.find(id="help")
    if not help_div:
        for sel in ("article", "main", ".article", "#article"):
            help_div = soup.select_one(sel)
            if help_div:
                break

    if not help_div:
        log.warning("No content container found for %s", url)
        return []

    start_el = help_div.select_one(CONTENT_START_SELECTOR)
    if not start_el:
        start_el = help_div.find("h1")
    if not start_el:
        for child in help_div.children:
            if isinstance(child, Tag):
                start_el = child
                break
        if not start_el:
            log.warning("No content found in #help for %s", url)
            return []

    elements: list[PageElement] = []
    current: PageElement | None = start_el
    while current:
        elements.append(current)
        current = current.find_next_sibling()

    return elements


def elements_to_markdown(
    elements: list[PageElement],
    pics_dir: Path | None,
    session: requests.Session | None,
    base_url: str,
) -> str:
    """Convert a list of content elements to a Markdown string."""
    img_cache: dict[str, str | None] = {}
    parts = []
    for el in elements:
        md = element_to_md(el, pics_dir, session, base_url, img_cache)
        if md:
            parts.append(md)

    result = "\n".join(parts)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip() + "\n"


# Phase 2: convert orchestrator


def convert_one(
    html_path: str,
    md_path: str,
    pics_dir: Path | None,
    session: requests.Session | None,
    base_url: str,
) -> bool:
    """Read a local HTML file and convert to Markdown. Returns True on success."""
    html_file = Path(html_path)
    if not html_file.exists():
        log.warning("HTML cache miss: %s", html_path)
        return False

    html = html_file.read_text(encoding="utf-8")
    elements = extract_content(html, base_url)
    if not elements:
        log.warning("No content extracted from %s", html_path)
        return False

    md_text = elements_to_markdown(elements, pics_dir, session, base_url)

    out = Path(md_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md_text, encoding="utf-8")
    return True


def run_convert(
    sitemap_path: str,
    force: bool = False,
    dry_run: bool = False,
) -> None:
    """Phase 2: convert cached HTML to Markdown."""
    urls = parse_sitemap(sitemap_path)
    root_prefix = _root_prefix_from_sitemap(sitemap_path)
    label = _label_from_sitemap(sitemap_path)
    md_output_dir = SITEMAP_DEFAULTS.get(sitemap_path, ("", label))[0]

    file_map = build_file_map(urls, root_prefix, md_output_dir, label)

    if dry_run:
        print(f"\n=== Convert dry run: {sitemap_path} ===")
        print(f"Total: {len(file_map)} files")
        html_cache = HTML_CACHE_ROOT / label
        cached = sum(1 for e in file_map if Path(e["html_path"]).exists())
        missing = len(file_map) - cached
        print(f"Cached HTML: {cached}, Missing: {missing}")
        for entry in file_map[:10]:
            exists = Path(entry["html_path"]).exists()
            mark = "✓" if exists else "✗"
            print(f"  [{entry['index']:4d}] {mark} {entry['html_path']}")
            print(f"         → {entry['file_path']}")
        if len(file_map) > 10:
            print(f"  ... ({len(file_map) - 10} more)")
        return

    # Progress log
    log_path = Path(md_output_dir) / ".convert.log"
    processed = _load_log(log_path) if not force else set()

    # Image session (only needed if images exist)
    img_session: requests.Session | None = None

    success = 0
    skipped = 0
    failed = 0

    for entry in file_map:
        url = entry["url"]
        if url in processed and not force:
            skipped += 1
            continue

        pics_dir = None
        if entry["chapter_folder"]:
            pics_dir = Path(md_output_dir) / entry["chapter_folder"] / "pics"

        # Lazy-init image session only when needed
        if img_session is None:
            img_session = requests.Session()

        img_session.headers.update({"User-Agent": get_user_agent(entry["index"])})

        base_url = url.rsplit("/", 1)[0] + "/" if "/" in url else url
        ok = convert_one(
            entry["html_path"], entry["file_path"],
            pics_dir, img_session, base_url,
        )
        if ok:
            success += 1
            _append_log(log_path, url)
            log.info("[%d/%d] OK: %s", success + skipped + failed, len(file_map), url)
        else:
            failed += 1
            log.error("[%d/%d] FAIL: %s", success + skipped + failed, len(file_map), url)

    log.info(
        "Done: %d success, %d skipped, %d failed (total %d)",
        success, skipped, failed, len(file_map),
    )


# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------


def run_debug(url: str) -> None:
    """Debug: fetch a single URL, print HTML structure, extract + convert."""
    session = requests.Session()
    session.headers.update({"User-Agent": get_user_agent()})

    print(f"Fetching: {url}")
    html = fetch_html(url, session)
    if html is None:
        print("FETCH FAILED")
        return

    soup = BeautifulSoup(html, "html.parser")
    help_div = soup.find(id="help")
    if not help_div:
        print("#help NOT FOUND")
        return

    print("#help found")

    h1 = help_div.select_one(CONTENT_START_SELECTOR)
    if not h1:
        h1 = help_div.find("h1")
    if h1:
        print(f"Start h1: {h1.get_text(strip=True)[:80]}")

    tables = help_div.find_all("table")
    imgs = help_div.find_all("img")
    pres = help_div.find_all("pre")
    ps = help_div.find_all("p")
    print(f"Tables: {len(tables)}, Imgs: {len(imgs)}, Pre: {len(pres)}, P: {len(ps)}")

    print("\n--- Tables ---")
    for i, t in enumerate(tables):
        thead = t.find("thead")
        rows = t.find_all("tr")
        first_cell = rows[0].find(["td", "th"]) if rows else None
        cell_text = first_cell.get_text(strip=True)[:60] if first_cell else "(empty)"
        has_code = bool(t.find("code") or t.find("pre"))
        print(f"  Table {i}: thead={bool(thead)}, rows={len(rows)}, "
              f"code={has_code}, first: {cell_text}")

    print("\n--- Images ---")
    for i, img in enumerate(imgs[:10]):
        src = img.get("src", "")
        alt = img.get("alt", "")
        next_p = img.find_next_sibling("p")
        next_p_text = next_p.get_text(strip=True)[:60] if next_p else "(no next p)"
        print(f"  Img {i}: src={src[:60]}, alt={alt[:40]}, next_p: {next_p_text}")

    print("\n--- Extraction ---")
    elements = extract_content(html, url)
    print(f"Extracted {len(elements)} elements")

    base_url = url.rsplit("/", 1)[0] + "/" if "/" in url else url
    md_text = elements_to_markdown(elements, None, session, base_url)
    print(f"\n--- Markdown output ({len(md_text)} chars) ---")
    print(md_text[:3000])
    if len(md_text) > 3000:
        print(f"\n... ({len(md_text) - 3000} more chars)")


# ---------------------------------------------------------------------------
# Progress log helpers
# ---------------------------------------------------------------------------


def _load_log(log_path: Path) -> set[str]:
    """Load set of already-processed URLs from log file."""
    if not log_path.exists():
        return set()
    urls = set()
    for line in log_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            urls.add(line)
    return urls


def _append_log(log_path: Path, url: str) -> None:
    """Append a URL to the processing log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(url + "\n")


# ---------------------------------------------------------------------------
# Sitemap helpers
# ---------------------------------------------------------------------------


def _root_prefix_from_sitemap(sitemap_path: str) -> str:
    if "book" in sitemap_path:
        return "/en/book/"
    if "docs" in sitemap_path:
        return "/en/docs/"
    return "/"


def _label_from_sitemap(sitemap_path: str) -> str:
    if "book" in sitemap_path:
        return "book"
    if "docs" in sitemap_path:
        return "docs"
    return "index"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Two-phase MQL5 extraction: download HTML → convert to Markdown."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- download ---
    dl = sub.add_parser("download", help="Phase 1: download HTML from mql5.com")
    dl_group = dl.add_mutually_exclusive_group(required=True)
    dl_group.add_argument("--sitemap", help="Path to a sitemap XML file")
    dl_group.add_argument("--all", action="store_true", help="All known sitemaps")
    dl.add_argument("--force", action="store_true", help="Re-download all")
    dl.add_argument("--dry-run", action="store_true", help="Show plan without fetching")
    dl.add_argument("--random-ua", action="store_true",
                     help="Use random User-Agent per request (default: deterministic rotation)")
    dl.add_argument("--random-delay", action="store_true",
                     help="Random delay between requests (1×–3× base delay)")
    dl.add_argument("--user-agents-csv", metavar="CSV",
                     help="Import User-Agents from CSV file (must have 'user_agent' column)")

    # --- convert ---
    cv = sub.add_parser("convert", help="Phase 2: convert cached HTML to Markdown")
    cv_group = cv.add_mutually_exclusive_group(required=True)
    cv_group.add_argument("--sitemap", help="Path to a sitemap XML file")
    cv_group.add_argument("--all", action="store_true", help="All known sitemaps")
    cv.add_argument("--force", action="store_true", help="Re-convert all")
    cv.add_argument("--dry-run", action="store_true", help="Show plan without converting")

    # --- debug ---
    dbg = sub.add_parser("debug", help="Debug: fetch + analyze a single URL")
    dbg.add_argument("url", help="URL to debug")

    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )

    if args.command == "debug":
        run_debug(args.url)
        return

    targets = []
    if args.command == "download":
        if args.all:
            targets = list(SITEMAP_DEFAULTS.keys())
        else:
            targets = [args.sitemap]
        for st in targets:
            if not os.path.exists(st):
                log.warning("Sitemap not found: %s — skipping", st)
                continue
            run_download(st, force=args.force, dry_run=args.dry_run,
                         random_ua=args.random_ua, random_delay=args.random_delay,
                         user_agents_csv=args.user_agents_csv)

    elif args.command == "convert":
        if args.all:
            targets = list(SITEMAP_DEFAULTS.keys())
        else:
            targets = [args.sitemap]
        for st in targets:
            if not os.path.exists(st):
                log.warning("Sitemap not found: %s — skipping", st)
                continue
            run_convert(st, force=args.force, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
