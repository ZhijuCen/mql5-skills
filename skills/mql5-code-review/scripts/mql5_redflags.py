#!/usr/bin/env python3
"""mql5_redflags.py — static red-flag scanner for MQL5 EA source.

Static-only companion of the mql5-code-review skill: flags known
anti-patterns in *.mq5 / *.mqh sources with severity levels matching
the skill's review labels (blocking / important / nit).

Usage:
    python mql5_redflags.py scan FILE.mq5 [MORE.mq5 ...] [DIR ...]
    python mql5_redflags.py scan src/ --json -o findings.json
    python mql5_redflags.py --list-rules

Scanning a single .mq5 automatically pulls in its project-local module
tree (`#include "..."` resolved recursively; use --no-includes to
restrict the scan to exactly the paths given). Built-in/stdlib includes
(`#include <...>`) are never followed.

Exit codes:
    0  scan completed, no blocking findings
    1  scan completed, at least one blocking finding
    2  usage or I/O error

Scanner output is evidence, not conclusions: findings need human
review (false positives happen; false negatives always do).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Iterable

SEV_BLOCKING = "blocking"
SEV_IMPORTANT = "important"
SEV_NIT = "nit"

SEV_ICON = {SEV_BLOCKING: "\U0001F534", SEV_IMPORTANT: "\U0001F7E1", SEV_NIT: "\U0001F7E2"}

MAX_FINDINGS_PER_RULE = 5

# ---------------------------------------------------------------- rules meta

RULES = {
    "no-retcode-check": (SEV_BLOCKING,
        "CTrade order call: return discarded (blocking); bool-conditioned but "
        "no ResultRetcode verification (important)",
        "Check ResultRetcode()==TRADE_RETCODE_DONE — CTrade bool true only "
        "means the request was communicated, not accepted."),
    "object-cleanup-missing": (SEV_BLOCKING,
        "Chart objects created but no OnDeinit cleanup (or cleanup without delete)",
        "Delete your objects in OnDeinit via ObjectsDeleteAll(0, prefix) or a name loop."),
    "objects-delete-all-noprefix": (SEV_BLOCKING,
        "ObjectsDeleteAll() wipes the whole chart including user objects",
        "Scope cleanup to your object-name prefix: ObjectsDeleteAll(0, PREFIX)."),
    "notify-no-throttle": (SEV_BLOCKING,
        "Alert/SendNotification/SendMail in per-tick path without visible throttle guard",
        "Edge-trigger + cooldown + daily budget before notifying (gui-ux-review §5)."),
    "trade-in-oninit": (SEV_BLOCKING,
        "Order/position call inside OnInit — no valid tick yet",
        "Wait for the first OnTick; OnInit should only configure."),
    "sleep-in-event": (SEV_IMPORTANT,
        "Sleep() inside an event handler blocks the terminal event thread",
        "Use new-bar gating / state machines instead of sleeping."),
    "print-flood": (SEV_IMPORTANT,
        "Print/PrintFormat/Comment in OnTick — journal flood, real incidents drown",
        "Gate logs to new bar or state change; add a debug input."),
    "object-create-in-ontick": (SEV_IMPORTANT,
        "Object create/delete or per-tick ObjectSet without change check",
        "Create objects once in OnInit; update properties change-driven."),
    "chartredraw-in-ontick": (SEV_IMPORTANT,
        "ChartRedraw() in OnTick forces a repaint per tick",
        "Batch object updates; one ChartRedraw(false) per batch, or timer-driven."),
    "discarded-copy-return": (SEV_IMPORTANT,
        "Copy* return value (count/-1) discarded — stale/garbage data path",
        "Compare against the exact requested count; skip trading on mismatch."),
    "handle-release-missing": (SEV_IMPORTANT,
        "Indicator handles created but IndicatorRelease never called",
        "Release every handle in OnDeinit."),
    "ontick-no-newbar-guard": (SEV_IMPORTANT,
        "Trade logic in OnTick with no new-bar gate — full logic every tick",
        "Gate bar-close logic on an iTime() compare (indicator-review)."),
    "fileopen-no-check": (SEV_IMPORTANT,
        "FileOpen used but INVALID_HANDLE never checked",
        "Check FileOpen against INVALID_HANDLE; fail loudly."),
    "webrequest-usage": (SEV_NIT,
        "WebRequest — URL whitelist + error 4014 handling reminder",
        "Off the tick path; handle 4014; parse defensively."),
    "dll-import": (SEV_NIT,
        "DLL import — permission/security review reminder",
        "Justify the binary source; refuse third-party DLLs without a reason."),
    "hardcoded-symbol": (SEV_NIT,
        "Hardcoded symbol-name literal",
        "Use _Symbol or an input parameter."),
    "double-equality": (SEV_NIT,
        "Equality comparison on a price-like variable (sentinel-zero and "
        "enum-constant comparisons exempted)",
        "Compare with a 1-point tolerance (MathAbs(a-b) <= _Point)."),
    "todo-fixme": (SEV_NIT,
        "TODO/FIXME/XXX/HACK left in source",
        "Resolve or track externally before deployment."),
    "commented-code": (SEV_NIT,
        "3+ consecutive commented-out code lines (dead code)",
        "Delete; version control remembers."),
}

# ------------------------------------------------------------ masking

STRING_MASK_RE = re.compile(r'"(?:[^"\\]|\\.)*"')
LINE_COMMENT_RE = re.compile(r"//[^\n]*")
BLOCK_COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)

# handlers that constitute the per-tick / event hot paths
TICK_HANDLERS = ("OnTick", "OnTimer", "OnTradeTransaction", "OnChartEvent")
ALL_HANDLERS = ("OnInit", "OnDeinit", "OnTick", "OnTimer", "OnStart",
                "OnCalculate", "OnTrade", "OnTradeTransaction",
                "OnChartEvent", "OnTester", "OnTesterInit", "OnTesterPass")

HANDLER_RE = re.compile(
    r"(?:^|\n)\s*(?:void|int|double|bool|datetime|string|long)\s+"
    r"(" + "|".join(ALL_HANDLERS) + r")\s*\(")

INCLUDE_QUOTED_RE = re.compile(r'^\s*#include\s+"([^"]+)"', re.M)
TRADE_CALL_RE = re.compile(
    r"\.\s*(PositionOpen|PositionClose|PositionClosePartial|PositionCloseTicket"
    r"|PositionModify|Buy|Sell|BuyLimit|SellLimit|BuyStop|SellStop"
    r"|OrderModify|OrderDelete|OrderSend)\s*\(")

RETRECON_RE = re.compile(r"ResultRetcode|ResultOrder|ResultDeal")
GUARD_RE = re.compile(
    r"IsNewBar|isNewBar|lastBarTime|m_lastBar|prevBar|iTime\s*\("
    r"|AllowNotify|m_lastNotify|cooldown|Cooldown|throttle|Throttle"
    r"|notifyBudget|NewSignal|lastSignal", re.I)

COPY_FN_RE = re.compile(
    r"^\s*(CopyBuffer|CopyRates|CopyTime|CopyOpen|CopyHigh|CopyLow|CopyClose"
    r"|CopyTickVolume|CopyRealVolume|CopyTicks|CopyTicksRange)\s*\(")

INDICATOR_CREATE_RE = re.compile(
    r"\b(iMA|iRSI|iMACD|iADX|iATR|iBands|iCustom|iCCI|iMomentum|iOsMA"
    r"|iStochastic|iWPR|iDeMarker|iForce|iVolumes|iBullsPower|iBearsPower"
    r"|Ichimoku|iSAR|iEnvelopes|iAlligator|iFractals|iRVI|iStdDev)\s*\(")

NOTIFY_RE = re.compile(r"\b(Alert|SendNotification|SendMail|SendAppMessage)\s*\(")
SLEEP_RE = re.compile(r"\bSleep\s*\(")
PRINT_RE = re.compile(r"\b(Print|PrintFormat|Comment)\s*\(")
OBJECT_ANY_RE = re.compile(r"\b(ObjectCreate|ObjectSet\w+|ObjectDelete\w*)\s*\(")
OBJECT_CREATE_RE = re.compile(r"\b(ObjectCreate|ObjectsDeleteAll)\s*\(")
CHARTREDRAW_RE = re.compile(r"\bChartRedraw\s*\(")
OBJDELALL_RE = re.compile(r"\bObjectsDeleteAll\s*\(([^)]*)\)")
FILEOPEN_RE = re.compile(r"\bFileOpen\s*\(")
WEBREQUEST_RE = re.compile(r"\bWebRequest\s*\(")
DLL_IMPORT_RE = re.compile(r'^\s*#import\s+"[^"<]+\.dll"', re.I | re.M)
SYMBOL_RE = re.compile(
    r'"((?:XAUUSD|XAGUSD|EURUSD|GBPUSD|USDJPY|USDCAD|AUDUSD|NZDUSD|USDCHF'
    r"|EURJPY|GBPJPY|EURGBP|DE30|DAX30|US30|NAS100|SPX500|UK100|WTI|BRENT)"
    r'[A-Za-z0-9._]*)"', re.I)
DOUBLE_EQ_RE = re.compile(
    r"\b(bid|ask|price|entry|openPrice|closePrice|slPrice|tpPrice|sl|tp|atr"
    r"|rsi|mid|spread)\d*\s*(?<![=!<>])==(?!=)")
# exemptions for double-equality: sentinel-zero checks (sl == 0) and
# enum-constant comparisons (entry == DEAL_ENTRY_OUT — an enum named like
# a price variable)
DOUBLE_EQ_EXEMPT_RE = re.compile(r"==\s*(?:0(?:\.0+)?\b|[A-Z][A-Z0-9_]{2,}\b)")
PRINT_FAILCONTEXT_RE = re.compile(
    r"ResultRetcode|GetLastError|ResultOrder|ResultDeal|failed|\berror\b",
    re.I)
TODO_RE = re.compile(r"//.*\b(TODO|FIXME|XXX|HACK)\b")
COMMENTED_CODE_RE = re.compile(r"^\s*//(?!\s*[+|\-]|\s*$)(.*[;{}].*)$")


def resolve_include(inc: str, including_file: Path) -> Path | None:
    """Resolve a quoted #include target: relative to the including file
    first (MQL5 semantics), then to the cwd. Backslashes normalized."""
    inc_path = Path(inc.replace("\\", "/"))
    for base in (including_file.parent, Path.cwd()):
        candidate = base / inc_path
        if candidate.is_file():
            return candidate.resolve()
    return None


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    severity: str
    message: str
    code: str = ""


@dataclass
class RuleCount:
    count: int = 0
    suppressed: int = 0


def mask_code(text: str) -> str:
    """Blank comments and string contents, preserving offsets/newlines."""
    def keep_str(m: re.Match) -> str:
        s = m.group(0)
        return s[0] + "x" * (len(s) - 2) + s[-1]
    text = STRING_MASK_RE.sub(keep_str, text)
    text = BLOCK_COMMENT_RE.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), text)
    text = LINE_COMMENT_RE.sub(lambda m: " " * len(m.group(0)), text)
    return text


def handler_ranges(text: str) -> dict[str, tuple[int, int]]:
    """Handler name -> (start_line, end_line) 1-based, inclusive."""
    ranges: dict[str, tuple[int, int]] = {}
    for m in HANDLER_RE.finditer(text):
        name = m.group(1)
        if name in ranges:      # first occurrence only (redefinitions rare)
            continue
        brace = text.find("{", m.end() - 1)
        if brace < 0:
            continue
        depth = 0
        end = -1
        for i in range(brace, len(text)):
            c = text[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end < 0:
            continue
        start_line = text.count("\n", 0, m.start()) + 1
        end_line = text.count("\n", 0, end) + 1
        ranges[name] = (start_line, end_line)
    return ranges


class ScanState:
    def __init__(self, path: Path):
        self.path = path
        self.raw = path.read_text(encoding="utf-8", errors="replace")
        self.raw_lines = self.raw.splitlines()
        self.code = mask_code(self.raw)
        self.code_lines = self.code.splitlines()
        self.handlers = handler_ranges(self.code)
        self.findings: list[Finding] = []
        self.counts: dict[str, RuleCount] = {r: RuleCount() for r in RULES}

    # -- helpers -------------------------------------------------------
    def add(self, rule: str, line: int, message: str = "", code: str = "",
            severity: str | None = None):
        self.counts[rule].count += 1
        if self.counts[rule].count > MAX_FINDINGS_PER_RULE:
            self.counts[rule].suppressed += 1
            return
        sev = severity or RULES[rule][0]
        if not message:
            message = RULES[rule][1]
        snippet = code.strip()[:100] if code else \
            (self.raw_lines[line - 1].strip()[:100] if 0 < line <= len(self.raw_lines) else "")
        self.findings.append(Finding(str(self.path), line, rule, sev, message, snippet))

    def handler_of(self, line: int) -> str | None:
        for name, (s, e) in self.handlers.items():
            if s <= line <= e:
                return name
        return None

    def handler_lines(self, name: str) -> list[int]:
        if name not in self.handlers:
            return []
        s, e = self.handlers[name]
        return list(range(s, e + 1))


def scan_file(path: Path) -> ScanState:
    st = ScanState(path)
    code_lines = st.code_lines

    # ---- file-level rules ----
    if DLL_IMPORT_RE.search(st.raw):
        m = DLL_IMPORT_RE.search(st.raw)
        st.add("dll-import", st.raw.count("\n", 0, m.start()) + 1)

    for m in SYMBOL_RE.finditer(st.raw):
        st.add("hardcoded-symbol", st.raw.count("\n", 0, m.start()) + 1,
               f"symbol literal {m.group(0)}")

    for i, line in enumerate(code_lines, 1):
        if DOUBLE_EQ_RE.search(line) and not DOUBLE_EQ_EXEMPT_RE.search(line):
            st.add("double-equality", i)

    for i, line in enumerate(st.raw_lines, 1):
        if TODO_RE.search(line):
            st.add("todo-fixme", i)

    # commented-out code blocks (3+ consecutive code-ish comment lines)
    run_start = None
    run_len = 0
    for i, line in enumerate(st.raw_lines, 1):
        if COMMENTED_CODE_RE.match(line):
            if run_start is None:
                run_start, run_len = i, 1
            else:
                run_len += 1
        else:
            if run_start is not None and run_len >= 3:
                st.add("commented-code", run_start,
                       f"{run_len} consecutive commented-out code lines")
            run_start, run_len = None, 0
    if run_start is not None and run_len >= 3:
        st.add("commented-code", run_start,
               f"{run_len} consecutive commented-out code lines")

    # ---- trade call rules ----
    # Calibration notes (from a real-world EA review, 6 FP / 5 TP on the
    # first run):
    #  - retcode check can legitimately live at the end of an if/else-if
    #    dispatch chain (up to ~24 lines below the call) — widen the window
    #    for calls whose return is consumed (assigned / conditioned);
    #  - a bool-conditioned call without retcode verification is still a gap
    #    (CTrade bool true = communicated, not accepted) but not blocking;
    #  - a discarded return stays blocking (silent failure path).
    trade_lines = [i for i, l in enumerate(code_lines, 1) if TRADE_CALL_RE.search(l)]
    for ln in trade_lines:
        if st.handler_of(ln) == "OnInit":
            st.add("trade-in-oninit", ln)
        line = code_lines[ln - 1]
        stripped = line.strip()
        fn = TRADE_CALL_RE.search(line).group(1)
        prefix = line.split(fn)[0]
        assigned = "=" in prefix and not prefix.strip().startswith("if")
        in_if = bool(re.match(r"^if\s*\(", stripped))
        if not (assigned or in_if) and ln >= 2:
            prev = code_lines[ln - 2].strip()
            in_if = prev.endswith(("if (", "if("))
        window = code_lines[ln - 1: ln + 23]      # 24 lines ahead
        if any(RETRECON_RE.search(l) for l in window[:8]):
            continue                              # retcode verified close by
        if (assigned or in_if) and any(RETRECON_RE.search(l) for l in window[8:]):
            continue                              # verified after dispatch chain
        if assigned or in_if:
            st.add("no-retcode-check", ln,
                   f"{fn} result is {'conditioned' if in_if else 'assigned'}, but "
                   "no ResultRetcode verification — CTrade bool true only means "
                   "the request was communicated",
                   severity=SEV_IMPORTANT)
        else:
            st.add("no-retcode-check", ln,
                   f"{fn} return value discarded — no retcode or failure handling")

    # ---- OnTick / event-handler rules ----
    for h in TICK_HANDLERS:
        hlines = st.handler_lines(h)
        if not hlines:
            continue
        body = [code_lines[i - 1] for i in hlines if i <= len(code_lines)]
        for ln in hlines:
            if ln > len(code_lines):
                break
            line = code_lines[ln - 1]
            if SLEEP_RE.search(line):
                st.add("sleep-in-event", ln, f"Sleep() in {h}")
            if h == "OnTick" and PRINT_RE.search(line):
                # failure-path logs (retcode/error context) are mandated by
                # the skill's diagnosability rules — exempt them
                ctx = " ".join(code_lines[max(0, ln - 4):ln]) + " " + st.raw_lines[ln - 1]
                if not PRINT_FAILCONTEXT_RE.search(ctx):
                    st.add("print-flood", ln, "per-tick Print/PrintFormat/Comment")
            if h == "OnTick" and OBJECT_CREATE_RE.search(line):
                st.add("object-create-in-ontick", ln, f"object create/delete in {h}")
            if h == "OnTick" and CHARTREDRAW_RE.search(line):
                st.add("chartredraw-in-ontick", ln, f"ChartRedraw() in {h}")
            nm = NOTIFY_RE.search(line)
            if nm and h in ("OnTick", "OnTimer", "OnTradeTransaction"):
                has_guard = any(GUARD_RE.search(b) for b in body)
                if has_guard:
                    st.add("notify-no-throttle", ln,
                           f"{nm.group(1)} in {h}: guard tokens present — verify "
                           "edge+cooldown+budget (downgrade to important if verified)",
                           severity=SEV_IMPORTANT)
                else:
                    st.add("notify-no-throttle", ln,
                           f"{nm.group(1)} in {h} with no visible throttle guard")
        # new-bar gate for trade logic
        if h == "OnTick" and any(TRADE_CALL_RE.search(b) for b in body):
            if not any(GUARD_RE.search(b) for b in body):
                start = st.handlers["OnTick"][0]
                st.add("ontick-no-newbar-guard", start,
                       "trade calls in OnTick, no new-bar/state gate visible")

    # ---- object cleanup rules ----
    if OBJECT_ANY_RE.search(st.code):
        if "OnDeinit" not in st.handlers:
            m = OBJECT_ANY_RE.search(st.code)
            st.add("object-cleanup-missing", st.code.count("\n", 0, m.start()) + 1,
                   "objects created, no OnDeinit handler at all")
        else:
            deinit_body = "\n".join(code_lines[i - 1] for i in st.handler_lines("OnDeinit"))
            if not re.search(r"ObjectsDeleteAll|ObjectDelete", deinit_body):
                st.add("object-cleanup-missing", st.handlers["OnDeinit"][0],
                       "OnDeinit exists but deletes no objects")

    for m in OBJDELALL_RE.finditer(st.code):
        args = m.group(1).strip()
        line = st.code.count("\n", 0, m.start()) + 1
        if "," not in args:
            st.add("objects-delete-all-noprefix", line,
                   "ObjectsDeleteAll with a single argument wipes the whole chart")
        else:
            prefix = args.split(",", 1)[1].strip()
            if prefix in ('""', "''"):
                st.add("objects-delete-all-noprefix", line,
                       "ObjectsDeleteAll with an empty prefix wipes the whole chart")

    # ---- copy-return rules ----
    for i, line in enumerate(code_lines, 1):
        m = COPY_FN_RE.match(line)
        if not m:
            continue
        if "=" in line.split(m.group(1))[0]:
            continue                     # assigned to something
        prev = code_lines[i - 2] if i >= 2 else ""
        if prev.rstrip().endswith(("if (", "if(", "&&", "||", ",")):
            continue                     # part of a condition
        st.add("discarded-copy-return", i, f"{m.group(1)}() return value discarded")

    # ---- handle release ----
    if INDICATOR_CREATE_RE.search(st.code) and "IndicatorRelease" not in st.code:
        m = INDICATOR_CREATE_RE.search(st.code)
        st.add("handle-release-missing", st.code.count("\n", 0, m.start()) + 1,
               "indicator handle created, IndicatorRelease never used")

    # ---- file I/O ----
    if FILEOPEN_RE.search(st.code) and "INVALID_HANDLE" not in st.code:
        m = FILEOPEN_RE.search(st.code)
        st.add("fileopen-no-check", st.code.count("\n", 0, m.start()) + 1)

    # ---- web request ----
    for m in WEBREQUEST_RE.finditer(st.raw):
        st.add("webrequest-usage", st.raw.count("\n", 0, m.start()) + 1)

    return st


# ---------------------------------------------------------------- output

def render_text(states: Iterable[ScanState]) -> str:
    out: list[str] = []
    total = {SEV_BLOCKING: 0, SEV_IMPORTANT: 0, SEV_NIT: 0}
    for st in states:
        n = len(st.findings)
        by = {s: sum(1 for f in st.findings if f.severity == s) for s in total}
        for s in total:
            total[s] += by[s]
        out.append(f"== {st.path}  ({n} findings: "
                   f"{by[SEV_BLOCKING]} blocking, {by[SEV_IMPORTANT]} important, "
                   f"{by[SEV_NIT]} nit)")
        for f in sorted(st.findings, key=lambda f: (f.line, f.rule)):
            out.append(f"  {SEV_ICON[f.severity]} [{f.severity}] {f.rule}  "
                       f"{st.path.name}:{f.line}")
            out.append(f"      {f.message}")
            if f.code:
                out.append(f"      > {f.code}")
        for rule, rc in sorted(st.counts.items()):
            if rc.suppressed:
                out.append(f"  … {rule}: {rc.suppressed} more finding(s) suppressed "
                           f"(cap {MAX_FINDINGS_PER_RULE}/rule)")
        out.append("")
    out.append(f"summary: {sum(len(s.findings) for s in states)} findings "
               f"(after per-rule cap) — {total[SEV_BLOCKING]} blocking, "
               f"{total[SEV_IMPORTANT]} important, {total[SEV_NIT]} nit")
    return "\n".join(out)


def render_json(states: Iterable[ScanState]) -> str:
    payload = {
        "tool": "mql5_redflags",
        "files": [],
        "summary": {SEV_BLOCKING: 0, SEV_IMPORTANT: 0, SEV_NIT: 0},
    }
    for st in states:
        payload["files"].append({
            "file": str(st.path),
            "findings": [asdict(f) for f in st.findings],
            "suppressed": {r: rc.suppressed for r, rc in st.counts.items() if rc.suppressed},
        })
        for f in st.findings:
            payload["summary"][f.severity] += 1
    return json.dumps(payload, indent=2)


def list_rules() -> str:
    out = ["mql5_redflags rules:", ""]
    for rid, (sev, desc, fix) in RULES.items():
        out.append(f"  {SEV_ICON[sev]} [{sev:>9}] {rid:<28} {desc}")
        out.append(f"      fix: {fix}")
    return "\n".join(out)


def collect_files(args_paths: list[str], follow_includes: bool = True) -> list[Path]:
    """Expand CLI paths into the scan set.

    Directories contribute every *.mq5/*.mqh below them (rglob).
    Files are scanned directly, and — when follow_includes is True —
    their QUOTED includes (`#include "..."`, project-local by MQL5
    convention) are resolved and pulled in recursively, so scanning a
    single .mq5 covers its whole module tree. Angle-bracket includes
    (`#include <Trade\\Trade.mqh>` — stdlib) are NOT followed.
    """
    files: list[Path] = []
    seen: set[Path] = set()

    def add(p: Path):
        rp = p.resolve()
        if rp in seen:
            return
        seen.add(rp)
        files.append(rp)
        if not follow_includes or p.suffix.lower() not in (".mq5", ".mqh"):
            return
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return
        for m in INCLUDE_QUOTED_RE.finditer(text):
            target = resolve_include(m.group(1), p)
            if target is None:
                # not a finding: the file may legitimately live in the
                # MQL5 tree; note it so coverage gaps stay visible
                print(f"note: unresolved #include \"{m.group(1)}\" in {p}",
                      file=sys.stderr)
                continue
            add(target)

    for p in args_paths:
        path = Path(p)
        if path.is_dir():
            for f in sorted(path.rglob("*.mq5")):
                add(f)
            for f in sorted(path.rglob("*.mqh")):
                add(f)
        elif path.is_file():
            add(path)
        else:
            print(f"error: no such file or directory: {p}", file=sys.stderr)
            sys.exit(2)
    return files


def main(argv: list[str]) -> int:
    if len(argv) == 1 and argv[0] in ("--list-rules", "list-rules", "rules"):
        print(list_rules())
        return 0

    ap = argparse.ArgumentParser(prog="mql5_redflags.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["scan"], help="scan — scan files/dirs")
    ap.add_argument("paths", nargs="+", help=".mq5/.mqh files or directories")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("-o", "--output", metavar="FILE", help="write output to FILE")
    ap.add_argument("--no-includes", action="store_true",
                    help="do not follow quoted #include directives")
    args = ap.parse_args(argv)

    files = collect_files(args.paths, follow_includes=not args.no_includes)
    if not files:
        print("error: no .mq5/.mqh files found", file=sys.stderr)
        return 2

    states = [scan_file(f) for f in files]
    text = render_json(states) if args.json else render_text(states)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"written: {args.output}")
    else:
        print(text)

    blocking = sum(1 for st in states for f in st.findings if f.severity == SEV_BLOCKING)
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
