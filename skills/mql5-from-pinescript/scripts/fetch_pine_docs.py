#!/usr/bin/env python3
"""Fetch Pine Script doc excerpts into references/pine-script-docs/.

Two source trees (discovered 2026-09-23):
  - User manual : https://www.tradingview.com/pine-script-docs/<section>/<page>
  - API reference: https://www.tradingview.com/pine-script-reference/v6/
                   (ONE page; per-symbol anchors #fun_ta.atr, #var_strategy.equity, ...)

Excerpt selection is driven by the mql5-from-pinescript porting
experience (ports 0001-0006) - see the README written alongside.
Requires: uv-managed deps (requests, beautifulsoup4).
"""
from __future__ import annotations

import os
import re
import sys

import requests
from bs4 import BeautifulSoup, NavigableString, Tag

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "references", "pine-script-docs")
OUT = os.path.normpath(OUT)
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# --- manual pages: (path, why-it-matters-for-porting) ----------------------
MANUAL = [
    ("concepts/bar-states", "barstate.isconfirmed/islast drove every closed-bar state machine (0001-0006)"),
    ("concepts/inputs", "input.* groups/inline/tooltip/time/source mapping to MQL5 inputs"),
    ("concepts/strategies", "strategy.* properties: fills, pyramiding, commission/slippage (ports 0004-0006)"),
    ("concepts/alerts", "alertcondition semantics gated our Alert() design (0001-0003)"),
    ("concepts/repainting", "HTF/non-repaint rules behind request.security choices (0001)"),
    ("concepts/other-timeframes-and-data", "request.security + lookahead_off = HTF wash mapping (0001)"),
    ("concepts/timeframes", "timeframe.from_seconds/in_seconds used for auto-HTF (0001)"),
    ("concepts/chart-information", "syminfo/chart.* reads (mintick, mincontract, bg/fg colors)"),
    ("language/execution-model", "per-bar execution order = our chronological state machines"),
    ("language/variable-declarations", "var / varip = the recursion & sequence state we ported"),
    ("language/type-system", "series vs simple typing behind x[k] lookbacks"),
    ("language/built-ins", "namespace map: ta/math/input/strategy/plot/... entry points"),
    ("faq/strategies", "broker-emulator & next-bar-open fill Q&A behind our execution model"),
    ("faq/variables-and-operators", "na propagation in ternaries/comparisons (ports lean on this)"),
]

# --- API reference anchor groups: (filename, [anchor id patterns]) ---------
ANCHOR_FILES = [
    ("reference-ta.md",       [r"^fun_ta\."]),
    ("reference-strategy.md", [r"^fun_strategy\.", r"^var_strategy\."]),
    ("reference-input.md",    [r"^fun_input\."]),
    ("reference-plotting.md", [r"^fun_plot", r"^fun_fill", r"^fun_hline",
                               r"^fun_barcolor", r"^fun_bgcolor",
                               r"^enum_location", r"^enum_size", r"^enum_style"]),
    ("reference-drawing.md",  [r"^fun_label\.", r"^fun_table\.", r"^fun_line\."]),
    ("reference-misc.md", [r"^fun_color\.new$", r"^fun_nz$", r"^fun_alertcondition$",
                           r"^fun_math\.(abs|min|max|pow|round|sqrt|pi|sum)$",
                           r"^var_chart\.(bg_color|fg_color)$",
                           r"^var_syminfo\.(mintick|mincontract|tickerid)$",
                           r"^var_timeframe\.(from_seconds|in_seconds)$"]),
]

MD_BLOCK_TAGS = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ",
                 "h5": "##### ", "li": "- ", "p": "", "tr": ""}


def html_to_md(node: Tag) -> str:
    out: list[str] = []

    def walk(el):
        for ch in el.children if isinstance(el, Tag) else []:
            if isinstance(ch, NavigableString):
                continue
            if not isinstance(ch, Tag):
                continue
            name = ch.name
            if name == "pre":
                code = ch.get_text()
                out.append("```\n" + code.rstrip() + "\n```\n")
                continue
            if name == "code" and not any(c.name == "pre" for c in [ch.parent]):
                out.append("`" + ch.get_text().strip() + "`")
                continue
            if name in ("strong", "b"):
                out.append("**" + ch.get_text() + "**")
                continue
            if name == "table":
                rows = []
                for tr in ch.find_all("tr"):
                    cells = [c.get_text(" ", strip=True).replace("|", "\\|")
                             for c in tr.find_all(["th", "td"])]
                    if cells:
                        rows.append("| " + " | ".join(cells) + " |")
                if rows:
                    out.append("\n".join(rows) + "\n")
                continue
            if name in MD_BLOCK_TAGS:
                text = ch.get_text(" ", strip=True)
                if text:
                    out.append(MD_BLOCK_TAGS[name] + text + ("\n" if name != "p" else "\n\n"))
                continue
            if name in ("ul", "ol", "div", "section", "article", "aside",
                        "span", "a", "em", "i", "dl", "dd", "dt", "figure",
                        "figcaption", "hr", "br", "blockquote"):
                if name in ("a", "em", "i", "span", "br", "hr"):
                    if name == "a":
                        out.append(ch.get_text())
                    elif name in ("em", "i"):
                        out.append("*" + ch.get_text() + "*")
                    elif name == "br":
                        out.append("\n")
                    continue
                walk(ch)
                continue
            walk(ch)

    walk(node)
    md = "".join(out)
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    return md.strip() + "\n"


def fetch(url: str) -> BeautifulSoup:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=45)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")


def manual_main(soup: BeautifulSoup) -> Tag:
    for sel in ("main", "article", '[class*="content"]', "body"):
        el = soup.select_one(sel)
        if el:
            return el
    return soup


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    fails = []
    written = []

    # ---- 1) manual pages ----
    for path, why in MANUAL:
        url = f"https://www.tradingview.com/pine-script-docs/{path}/"
        fname = path.replace("/", "-") + ".md"
        try:
            soup = fetch(url)
            md = html_to_md(manual_main(soup))
            # drop nav noise lines typical of the shell
            md = re.sub(r"(?im)^(on this page|table of contents|previous|next)\s*$", "", md)
            if len(md) < 500:
                fails.append(f"{path}: only {len(md)} chars")
                continue
            header = f"<!-- source: {url} | fetched 2026-09-23 | why: {why} -->\n\n"
            with open(os.path.join(OUT, fname), "w", encoding="utf-8") as fh:
                fh.write(header + md)
            written.append((fname, len(md), why))
            print(f"OK  {fname:52s} {len(md):6d}  {why[:50]}")
        except Exception as exc:  # noqa: BLE001
            fails.append(f"{path}: {exc}")
            print(f"ERR {path}: {exc}")

    # ---- 2) API reference anchors ----
    # /pine-script-reference/v6/ is a JS-only shell: its entries are
    # hydrated client-side into div.tv-pine-reference-item and are NOT
    # present in the HTML or any fetchable endpoint. The reference-*.md
    # excerpts are therefore a one-time browser-DOM extraction (committed
    # artifacts) - see references/pine-script-docs/README.md.
    ref_files = [f for f, _ in ANCHOR_FILES]
    missing_ref = [f for f in ref_files
                   if not os.path.exists(os.path.join(OUT, f))]
    if missing_ref:
        fails.append("missing reference excerpts (browser extraction needed, "
                     "see pine-script-docs/README.md): " + ", ".join(missing_ref))
    else:
        print(f"reference-*.md present ({len(ref_files)} files, browser "
              "DOM extraction - skipped; see README.md)")

    print(f"\n{len(written)} files written -> {OUT}")
    if fails:
        print("FAILURES:")
        for f in fails:
            print("  -", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
