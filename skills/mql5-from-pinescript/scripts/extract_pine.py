#!/usr/bin/env python3
"""Fetch the Pine Script source of a TradingView open-source script.

TradingView renders the code viewer client-side, but the underlying
publication page embeds the script's `script_id_part`, and the
`pine-facade` endpoint serves the raw source as plain JSON. No login and
no browser required for open-source scripts.

CLI convention (project-wide): SCRIPT.py SUB_COMMAND INPUT [OPTIONS] [-o OUT]
Sub-command is the first non-flag token; --json / -o follow INPUT.

Usage:
    python skills/mql5-from-pinescript/scripts/extract_pine.py fetch PAGE_URL [-o FILE] [--json]
    python skills/mql5-from-pinescript/scripts/extract_pine.py fetch PAGE_URL --check FILE

Exit codes: 0 ok, 1 fetch/parse error, 2 script source not accessible
(not open-source), 3 --check mismatch.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from urllib.parse import quote

import requests

FACADE = "https://pine-facade.tradingview.com/pine-facade/get/{sid}/1?no_4xx=true"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
SCRIPT_ID_RE = re.compile(r'"script_id_part"\s*:\s*"(PUB;[0-9a-f]+)"')


def get(url: str, **kw) -> requests.Response:
    resp = requests.get(url, headers={"User-Agent": UA}, timeout=30, **kw)
    resp.raise_for_status()
    return resp


def fetch(page_url: str) -> dict:
    """Return {url, script_id, name, version, access, source}."""
    html = get(page_url).text
    m = SCRIPT_ID_RE.search(html)
    if not m:
        raise RuntimeError("script_id_part not found — not a publication "
                           "script page, or the page layout changed")
    script_id = m.group(1)
    sid_enc = quote(script_id, safe="")
    data = get(FACADE.format(sid=sid_enc)).json()
    source = data.get("source")
    if source is None:
        raise RuntimeError(f"pine-facade returned no 'source' key: "
                           f"{sorted(data)}")
    return {
        "page": page_url,
        "script_id": script_id,
        "name": data.get("scriptName"),
        "version": data.get("version"),
        "access": data.get("scriptAccess"),
        "updated": data.get("updated"),
        "source": source,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sub", choices=["fetch"], help="sub-command")
    ap.add_argument("input", metavar="PAGE_URL",
                    help="TradingView script page URL")
    ap.add_argument("-o", "--out", metavar="FILE",
                    help="write Pine source to FILE")
    ap.add_argument("--check", metavar="FILE",
                    help="compare fetched source against FILE (LF-normalized)")
    ap.add_argument("--json", action="store_true",
                    help="print metadata + source as JSON")
    args = ap.parse_args()

    try:
        rec = fetch(args.input)
    except Exception as exc:  # noqa: BLE001 - CLI boundary
        print(f"error: {exc}", file=sys.stderr)
        return 1

    open_like = rec["access"] == "open_no_auth"
    if not open_like:
        print(f"warning: scriptAccess={rec['access']!r} — source may be "
              "masked or require login", file=sys.stderr)

    src = rec["source"]
    lf = src.replace("\r\n", "\n").replace("\r", "\n")

    if args.check:
        try:
            with open(args.check, "r", encoding="utf-8") as fh:
                ref = fh.read().replace("\r\n", "\n").replace("\r", "\n")
        except OSError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if ref.strip() == lf.strip():
            print(f"OK  {args.check} matches {rec['name']} "
                  f"(v{rec['version']})")
            return 0
        print(f"MISMATCH  {args.check} != published source of "
              f"{rec['name']}", file=sys.stderr)
        return 3

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(lf)
        print(f"wrote {args.out}: {lf.count(chr(10)) + 1} lines "
              f"({rec['name']}, v{rec['version']}, {rec['access']})")
    elif args.json:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    else:
        sys.stdout.write(lf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
