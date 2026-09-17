#!/usr/bin/env python3
"""
MQL5 development helper: compile, check, deploy, list, status,
init-ini (generate a Tester INI skeleton from .mq5 inputs),
tester (headless single test or Grid optimization via an INI file).

Supports Windows 10+ natively (PowerShell) and Linux/Wine.

Paths are NEVER auto-detected.  MT5_BASE / MQL5_DIR / WINE_DISK_ROOT
must come from the environment or the project-root ``.env`` file
(walk-up from cwd, e.g. ``$PROJECT_ROOT/.env``).  WINE_DISK_ROOT is
required on Unix (Linux/macOS) only — the drive letter that maps to
``/`` under Wine (e.g. ``Z``); it is ignored on Windows.

Usage:
    python skills/mql5/scripts/mql5_helper.py compile FILE.mq5
    python skills/mql5/scripts/mql5_helper.py check FILE.mq5
    python skills/mql5/scripts/mql5_helper.py deploy FILE.mq5
    python skills/mql5/scripts/mql5_helper.py status
    python skills/mql5/scripts/mql5_helper.py list
    python skills/mql5/scripts/mql5_helper.py init-ini FILE.mq5 [OPTS]
    python skills/mql5/scripts/mql5_helper.py tester INI [OPTS]

deploy compiles the .mq5 first, then copies the resulting .ex5 into
the correct MQL5 sub-directory (Experts / Indicators / Scripts /
Services) based on event functions found in the source code.

init-ini parses every ``input`` / ``sinput`` declaration in the .mq5
source and emits a [Tester]/[TesterInputs] INI skeleton where each
line is ``name=default||start||step||stop||Y|N`` — inputs omitted
from [TesterInputs] silently fall back to EA source defaults, so the
skeleton lists ALL of them.

tester runs a Strategy Tester single test or optimization headlessly
(Optimization=0: single; 1: complete Grid; 2: genetic; 3: Market Watch).
It validates and normalizes the INI, stages it at a space-free Windows path,
launches the terminal against a dedicated runner instance (cloned
from MT5_BASE on first use, so the user's GUI terminal is not
disturbed), polls process exit + journal + report, copies the report
artifacts to -o OUTDIR and prints the parsed summary.  Pitfall list
and observed error strings: references/quick-ref-tester-automation.md.
"""

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TYPE_DIRS: dict[str, str] = {
    "expert": "Experts",
    "indicator": "Indicators",
    "script": "Scripts",
    "service": "Services",
    "include": "Include",
}

IS_WINDOWS = sys.platform == "win32"

# Variables loaded from the environment / project-root .env.
# WINE_DISK_ROOT is required on Unix only (Windows ignores it).
_ENV_KEYS = ("MT5_BASE", "MQL5_DIR", "WINE_DISK_ROOT")


def _load_env(env_path: Optional[Path] = None) -> None:
    """Load MT5_BASE / MQL5_DIR / WINE_DISK_ROOT from a ``.env`` file.

    *env_path* — optional explicit path (``--env-file``).  When given,
    that file must exist (raises ``SystemExit(1)`` on missing or
    unreadable).  When ``None`` (default), walks up from ``Path.cwd()``
    and uses the first ``.env`` it finds (silent on miss — values may
    still come from the real environment).

    Supports ``KEY="VALUE" KEY2="VALUE2"`` on one line (space-separated),
    one-var-per-line, or mixes thereof, using ``shlex.split`` for quoting.
    Existing environment variables take precedence via ``setdefault``.
    """
    candidates: list[Path] = []
    if env_path is not None:
        env_path = Path(env_path)
        if not env_path.is_file():
            print(f"Error: --env-file not found: {env_path}")
            sys.exit(1)
        candidates.append(env_path)
    else:
        d = Path.cwd()
        while True:
            ef = d / ".env"
            if ef.is_file():
                candidates.append(ef)
                break
            parent = d.parent
            if parent == d:
                break
            d = parent

    for ef in candidates:
        try:
            text = ef.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            print(f"Error: cannot read {ef}: {e}")
            sys.exit(1)
        import shlex

        for token in shlex.split(text):
            if "=" not in token:
                continue
            idx = token.index("=")
            key = token[:idx]
            val = token[idx + 1 :]
            if key in _ENV_KEYS:
                os.environ.setdefault(key, val)


# ---------------------------------------------------------------------------
# Path resolution  — STRICTLY from env / .env.  No directory guessing.
# ---------------------------------------------------------------------------


def _resolve_paths() -> tuple[Path, Path]:
    """Return (MT5_BASE, MQL5_DIR) from env vars or the project ``.env``.

    Both values are required — the script no longer scans Program
    Files or walks the cwd tree for an MQL5 installation.  When a
    value is missing it exits with an error naming the variable,
    instead of guessing.
    """
    missing = [
        k for k in ("MT5_BASE", "MQL5_DIR") if not os.environ.get(k)
    ]
    if missing:
        print(
            "Error: required variable(s) not set: "
            + ", ".join(missing)
        )
        print(
            "  Define them in the project-root `.env` (or export them in "
            "the environment), e.g.:"
        )
        print('    MT5_BASE="C:/Program Files/MetaTrader 5"')
        print('    MQL5_DIR="C:/Program Files/MetaTrader 5/MQL5"')
        sys.exit(1)
    return Path(os.environ["MT5_BASE"]), Path(os.environ["MQL5_DIR"])


# ---------------------------------------------------------------------------
# Module-level defaults — see _apply_paths() / main() for actual logic.
# These placeholders exist only so `from mql5_helper import MT5_BASE` does
# not blow up; main() always re-resolves and assigns before any command.
# ---------------------------------------------------------------------------
MT5_BASE: Path = Path()
MQL5_DIR: Path = Path()


def _apply_paths(env_path: Optional[Path] = None) -> None:
    """Load ``.env`` (if needed) and re-resolve ``MT5_BASE`` / ``MQL5_DIR``.

    Updates module globals so all commands see the latest values.
    """
    _load_env(env_path)
    global MT5_BASE, MQL5_DIR
    MT5_BASE, MQL5_DIR = _resolve_paths()

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def _to_editor_path(path: Path) -> str:
    """Return *path* in the format the MetaEditor CLI expects.

    On Windows native: the native path (backslashes).
    On Unix/Wine: prefix with ``WINE_DISK_ROOT`` (the drive letter
    that maps to ``/`` under Wine, e.g. ``Z``) and keep forward
    slashes, e.g. ``Z://home/USER/path/to/file.mq5``.  Requires
    WINE_DISK_ROOT to be set; missing it is an error (never guessed
    from the Wine prefix).
    """
    if IS_WINDOWS:
        return str(path)
    drive = os.environ.get("WINE_DISK_ROOT", "").strip()
    if not drive:
        print(
            "Error: WINE_DISK_ROOT is not set. "
            "Set it in the project-root `.env` (the drive letter that "
            "maps to `/` under Wine, e.g. `Z`)."
        )
        sys.exit(1)
    drive = drive.rstrip(":")  # tolerate "Z:" as well as "Z"
    # Absolute path with forward slashes, prefixed by the drive letter
    # and a double slash:  Z://home/user/...
    return f"{drive}://{path.as_posix().removeprefix('/')}"


def _build_editor_cmd(editor: Path, flags: list[str]) -> list[str]:
    """Return ``subprocess.run`` command args for the target platform."""
    if IS_WINDOWS:
        return [str(editor), *flags]
    return ["wine", str(editor), *flags]


# ---------------------------------------------------------------------------
# Type detection
# ---------------------------------------------------------------------------


def detect_type(file_path: Path) -> str:
    """Infer program type from path segments."""
    for p in file_path.parts:
        pl = p.lower()
        if pl in ("experts", "advisor", "advisors"):
            return "expert"
        if pl in ("indicators",):
            return "indicator"
        if pl in ("scripts",):
            return "script"
        if pl in ("services",):
            return "service"
        if pl in ("include",):
            return "include"
    return "expert"


# Event-function / property signatures that uniquely identify each MQL5
# program type.  A match in the source content takes priority over the
# path-based guess from detect_type().
#
# Detection order matters: services are checked FIRST because they also
# contain OnTimer (shared with experts) — the #property service directive
# is the decisive signal.

_SERVICE_MARKERS: list[str] = [
    r"#property\s+service",
]


def detect_type_from_source(file_path: Path) -> str:
    """Detect program type by analysing the ``.mq5`` source content.

    Reads the source file once and checks for event functions and
    preprocessor directives that are unique to each program type.

    Detection rules (in order of priority):

    1. **Service** — ``#property service`` present  →  ``service``
    2. **Service** — ``OnStart`` + ``OnTimer`` + ``OnDeinit``
       (no ``OnTick`` / ``OnCalculate``)  →  ``service``
    3. **Indicator** — ``OnCalculate`` present  →  ``indicator``
    4. **Expert** — ``OnTick`` present  →  ``expert``
    5. **Script** — ``OnStart`` present  →  ``script``
    6. Fallback: ``expert``

    Returns a key that maps to ``TYPE_DIRS`` (``expert``, ``indicator``,
    ``script``, ``service``).
    """
    import re

    try:
        text = file_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "expert"

    # --- service markers -------------------------------------------------
    for pat in _SERVICE_MARKERS:
        if re.search(pat, text):
            return "service"

    # Collect which named events appear in the source
    has = {name: False for name in (
        "OnStart", "OnTimer", "OnDeinit", "OnTick",
        "OnTrade", "OnChartEvent", "OnCalculate",
    )}
    for name in has:
        if re.search(rf"\b{name}\b", text):
            has[name] = True

    # Service heuristic: OnStart + OnTimer + OnDeinit, but no OnTick/OnCalculate
    if has["OnStart"] and has["OnTimer"] and has["OnDeinit"]:
        if not has["OnTick"] and not has["OnCalculate"]:
            return "service"

    # --- indicator (OnCalculate is unique to indicators) -----------------
    if has["OnCalculate"]:
        return "indicator"

    # --- expert (OnTick is unique to experts) ---------------------------
    if has["OnTick"]:
        return "expert"

    # --- script (OnStart only, no timer/service signals) ----------------
    if has["OnStart"]:
        return "script"

    return "expert"


def resolve_type(src: Path) -> str:
    """Return the program type, preferring source-content analysis.

    If *src* is a ``.mq5`` file, the content is scanned for event
    functions / ``#property service``.  Falls back to path-based
    ``detect_type()`` if the content scan cannot decide.
    """
    if src.suffix.lower() == ".mq5":
        return detect_type_from_source(src)
    return detect_type(src)


def _find_editor() -> Optional[Path]:
    """Locate ``MetaEditor64.exe`` in MT5_BASE."""
    for name in ("MetaEditor64.exe", "MetaEditor.exe"):
        p = MT5_BASE / name
        if p.is_file():
            return p
    return None


# ---------------------------------------------------------------------------
# Compile-freshness check
# ---------------------------------------------------------------------------


def _check_timestamps(
    t_before: float,
    ex5_path: Path,
    log_path: Path,
    *,
    expect_ex5: bool,
) -> bool:
    """Return True if expected outputs are fresher than *t_before*.

    *expect_ex5* — True for ``compile`` (must produce ``.ex5``);
    False for ``check`` (``.ex5`` optional, ``.log`` mandatory).

    Prints diagnostic messages on failure.
    """
    issues: list[str] = []

    if expect_ex5:
        if ex5_path.exists() and ex5_path.stat().st_mtime > t_before:
            elapsed = time.time() - ex5_path.stat().st_mtime
            print(f"  ✓ {ex5_path}  ({ex5_path.stat().st_mtime - t_before:.1f}s after start)")
        else:
            what = "not found" if not ex5_path.exists() else "stale (mtime before compile)"
            issues.append(f"  ✗ {ex5_path} — {what}")

    if log_path.exists() and log_path.stat().st_mtime > t_before:
        elapsed = time.time() - log_path.stat().st_mtime
        print(f"  ✓ {log_path}  ({log_path.stat().st_mtime - t_before:.1f}s after start)")
    else:
        what = "not found" if not log_path.exists() else "stale (mtime before compile)"
        issues.append(f"  ✗ {log_path} — {what}")

    if issues:
        print("\n".join(issues))
        return False
    return True


def _print_log(log_path: Path, label: str = "Compilation log") -> None:
    """Print last 30 lines of a MetaEditor ``.log`` file.

    MetaEditor logs are UTF-16LE on Windows; auto-detect encoding.
    """
    try:
        raw = log_path.read_bytes()
    except OSError:
        return
    # Detect UTF-16LE BOM (\xff\xfe) or null-byte pattern
    if raw[:2] == b"\xff\xfe" or b"\x00" in raw[: min(len(raw), 1024)]:
        log_text = raw.decode("utf-16-le", errors="replace")
    else:
        log_text = raw.decode("utf-8", errors="replace")
    lines = log_text.strip().splitlines()
    if lines:
        print(f"\n{label} ({len(lines)} lines):")
        for line in lines[-30:]:
            print(f"  {line}")


# ---------------------------------------------------------------------------
# Core: run editor on the SOURCE path + freshness check
# ---------------------------------------------------------------------------


def _run_editor(src: Path, extra_flags: list[str], *, expect_ex5: bool) -> int:
    """Invoke MetaEditor on *src* directly (no deploy) and verify freshness.

    Compiles the source file in place — it does NOT copy *src* into the
    MQL5 tree.  Output artifacts (``.ex5`` / ``.log``) land next to the
    source, matching MetaEditor's CLI behaviour.  Use ``deploy`` if you
    want the file copied into the MQL5 directory first.

    *extra_flags* — additional CLI flags for the editor (e.g. ``/s``).
    *expect_ex5* — True for ``compile``, False for ``check``.

    On Windows, MetaEditor64.exe returns immediately and compiles in the
    background; we poll for the ``.log`` file with a 30 s timeout.
    On Wine, the GUI runs synchronously so ``subprocess.run`` blocks until
    the compile finishes.
    """
    src = src.resolve()
    if not src.is_file():
        print(f"Error: {src} not found")
        return 1

    editor = _find_editor()
    if editor is None:
        print(f"Error: MetaEditor.exe not found in {MT5_BASE}")
        return 1

    # Pre-remove stale outputs so they can't fake freshness
    t_before = time.time()
    ex5_path = src.with_suffix(".ex5")
    log_path = src.with_suffix(".log")
    for p in (ex5_path, log_path):
        if p.exists():
            p.unlink()

    # Build command — compile_arg points at the SOURCE file path.
    # NOTE: do NOT wrap the path in double quotes here.  With
    # subprocess we pass a pre-split argv list; wine (Linux/macOS)
    # and CreateProcess (Windows) receive each element as exactly one
    # argument, and literal `"` characters become part of the path
    # string MetaEditor sees, making it unresolvable.  Quoting is the
    # shell's job, and we are not going through a shell.
    compile_arg = f'/compile:{_to_editor_path(src)}'
    cmd = _build_editor_cmd(editor, [compile_arg, "/log", *extra_flags])
    print(f"Running: {' '.join(cmd)}")

    # Run editor
    try:
        if IS_WINDOWS:
            # MetaEditor outputs UTF-16 binary on Windows; don't capture.
            result = subprocess.run(
                cmd,
                capture_output=False,
                timeout=60,
                cwd=str(editor.parent),
            )
        else:
            # Wine serialises GUI apps; capturing is safe.
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(editor.parent),
            )
    except FileNotFoundError:
        if IS_WINDOWS:
            print(f"Error: {cmd[0]} not found on PATH. Verify MT5 installation.")
        else:
            print("Error: wine not found. Install wine or run on Windows.")
        return 1
    except subprocess.TimeoutExpired:
        print("Compile timed out (60s).")
        return 1

    # On Wine: show raw output immediately
    if not IS_WINDOWS:
        if result.stdout.strip():
            print(f"\n--- Editor stdout ---\n{result.stdout.rstrip()}")
        if result.stderr.strip():
            print(f"--- Editor stderr ---\n{result.stderr.rstrip()}")

    # Wait for output files (Windows: compile is async, poll up to 30 s)
    if IS_WINDOWS:
        _wait_for_compile(log_path, timeout=30)

    # Show log
    if log_path.exists():
        _print_log(log_path, "Compilation log" if expect_ex5 else "Syntax-check log")

    # Freshness verification
    print("\nFile freshness check:")
    fresh = _check_timestamps(t_before, ex5_path, log_path, expect_ex5=expect_ex5)
    if not fresh:
        print("\nCompilation may not have succeeded.  Expected output file(s) are missing")
        print("or were not updated.  Check the editor log above for errors.")
        return 1 if expect_ex5 else result.returncode
    print("  ✓ All expected outputs updated — compile succeeded\n"
          if expect_ex5 else
          "  ✓ Log updated — syntax check completed\n")
    # Success is decided by the freshness check above, NOT by the
    # subprocess returncode: on Wine, MetaEditor is a GUI app and its
    # exit code is unreliable (it can be non-zero even on success).
    return 0


def _wait_for_compile(log_path: Path, timeout: int = 30) -> None:
    """Poll for the ``.log`` file up to *timeout* seconds.

    On Windows, MetaEditor compiles asynchronously in a background GUI
    process.  We block here so the caller can check freshness afterward.
    """
    deadline = time.time() + timeout
    polled = 0.0
    while time.time() < deadline:
        if log_path.exists():
            elapsed = time.time() - (deadline - timeout)
            if polled > 0.5:
                print(f"  (waited {elapsed:.1f}s for compile output)")
            return
        time.sleep(0.3)
        polled += 0.3
    print(f"  (timed out after {timeout}s waiting for {log_path.name})")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_compile(args: argparse.Namespace) -> int:
    """Compile an MQ5 file (produces .ex5 + .log)."""
    return _run_editor(Path(args.file), extra_flags=[], expect_ex5=True)


def cmd_check(args: argparse.Namespace) -> int:
    """Syntax-check an MQ5 file without full compilation (/s flag)."""
    return _run_editor(Path(args.file), extra_flags=["/s"], expect_ex5=False)


def cmd_deploy(args: argparse.Namespace) -> int:
    """Compile an ``.mq5`` file then deploy the resulting ``.ex5`` to MQL5.

    Steps:

    1. Compile the source ``.mq5`` (via ``_run_editor``).
    2. Analyse the source content for event functions / ``#property service``
       to determine the correct MQL5 sub-directory.
    3. Copy the ``.ex5`` file into ``MQL5_DIR/<subdir>/``.

    The destination sub-directory is chosen by ``resolve_type()``, which
    inspects the source file for type-specific markers:

    * ``#property service``  →  ``Services/``
    * ``OnCalculate``       →  ``Indicators/``
    * ``OnTick``            →  ``Experts/``
    * ``OnStart``           →  ``Scripts/``
    * fallback              →  ``Experts/``
    """
    src = Path(args.file).resolve()
    if not src.is_file():
        print(f"Error: {src} not found")
        return 1

    # --- Step 1: compile -------------------------------------------------
    print(f"Compiling {src.name} …")
    rc = _run_editor(src, extra_flags=[], expect_ex5=True)
    if rc != 0:
        print("Error: compilation failed — aborting deploy.")
        return rc

    ex5 = src.with_suffix(".ex5")
    if not ex5.is_file():
        print(f"Error: compiled .ex5 not found: {ex5}")
        return 1

    # --- Step 2: detect type from source content -------------------------
    ptype = resolve_type(src)
    dest_dir = MQL5_DIR / TYPE_DIRS.get(ptype, "Experts")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / ex5.name

    # --- Step 3: copy .ex5 -----------------------------------------------
    shutil.copy2(ex5, dest)
    print(f"\nDeployed: {ex5.name} → {dest}")
    print(f"Type:     {ptype}  (detected from source content)")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    """Show MT5 / MQL5 environment status."""
    platform_label = "Windows (native)" if IS_WINDOWS else "Linux (Wine)"
    print(f"MQL5 Helper — Status")
    print(f"  Platform:      {platform_label}")
    print(f"  MT5 Base:      {MT5_BASE}")
    print(f"  MQL5 Dir:      {MQL5_DIR}")
    print(f"  MQL5 exists:   {MQL5_DIR.exists()}")

    if MQL5_DIR.exists():
        for subdir in ("Experts", "Indicators", "Scripts", "Services", "Include"):
            d = MQL5_DIR / subdir
            if d.exists():
                mq5 = list(d.rglob("*.mq5"))
                ex5 = list(d.rglob("*.ex5"))
                print(f"    {subdir:12s}: {len(mq5)} .mq5, {len(ex5)} .ex5")

    editor = _find_editor()
    if editor:
        print(f"  Editor:        {editor}")
        print(f"    Exists:      ✓")
    else:
        print(f"  Editor:        (not found in {MT5_BASE})")

    print(f"  Terminal:      {MT5_BASE / 'terminal64.exe'}")
    print(f"    Exists:      {(MT5_BASE / 'terminal64.exe').exists()}")

    print()
    if IS_WINDOWS:
        print("  PowerShell compile template:")
        print(f'    & "{editor or MT5_BASE / "MetaEditor64.exe"}" /compile:"path\\to\\file.mq5" /log')
    else:
        drive = os.environ.get("WINE_DISK_ROOT", "").strip().rstrip(":")
        print("  Wine compile template (WINE_DISK_ROOT drive letter + double forward slash):")
        print(f'    wine "{editor or MT5_BASE / "MetaEditor64.exe"}" /compile:"{drive}://home/USER/path/to/file.mq5" /log')
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """List MQ5 source files in the MQL5 directory."""
    if not MQL5_DIR.exists():
        print(f"MQL5 directory not found: {MQL5_DIR}")
        return 1

    for subdir in ("Experts", "Indicators", "Scripts", "Services"):
        d = MQL5_DIR / subdir
        if not d.is_dir():
            continue
        files = sorted(d.rglob("*.mq5"))
        if files:
            print(f"\n{subdir}/")
            for f in files:
                rel = f.relative_to(d)
                print(f"  {rel}")
    return 0


# ---------------------------------------------------------------------------
# Tester automation — terminal64.exe /portable /config:<INI>
#
# Pitfall list this code encodes (details + error strings:
# references/quick-ref-tester-automation.md):
#   1. [Tester] Report=<name> writes <name>.htm(l) + PNGs into the
#      TERMINAL WORKING DIRECTORY (install root for /portable), not
#      the process CWD / MQL5\Files / the INI's dir.
#   2. /config:<path> must be a Windows-style ABSOLUTE path and
#      SPACE-FREE — a quoted path with spaces makes the terminal log
#      `cannot load config "..."` and boot as a plain GUI.
#   3. Single-instance lock: run against a dedicated cloned instance
#      (needs Bases\ + MQL5\; temp/logs/agent caches excludable).
#   4. UseLocal=1 is REQUIRED or no local agent spawns and the run
#      silently never starts.
#   5. Every [TesterInputs] line must be name=value||start||step||stop||Y|N;
#      omitted inputs silently fall back to EA source defaults.
#   6. Launch detached; completion = process exit + journal
#      successful test/optimization journal + report file present.
#      Optimization writes XML rather than HTML + PNGs. Poll, never sleep.
#   7. Journal logs\YYYYMMDD.log is UTF-16LE — decode before parsing.
#   8. INI written with CRLF defensively.
# ---------------------------------------------------------------------------

_TESTER_REQUIRED_KEYS = ("Expert", "Symbol", "Period", "FromDate", "ToDate")

MODEL_ENUM = {
    "0": "every tick (generated)",
    "1": "1-minute OHLC",
    "2": "open prices only",
    "4": "every tick based on real ticks (falls back to generated ticks "
         "when the broker history has none)",
}

OPTIMIZATION_ENUM = {
    "0": "disabled (single test)",
    "1": "slow complete algorithm (Grid / exhaustive parameter combinations)",
    "2": "fast genetic algorithm",
    "3": "all symbols selected in Market Watch",
}

# Artifact suffixes MT5 writes next to the report .htm(l) (pitfall #1).
_REPORT_PNG_SUFFIXES = (".png", "-hst.png", "-mfemae.png", "-holding.png")


def _posix_to_win(path: Path) -> str:
    """Convert a POSIX path to a Windows path for MT5 CLI flags.

    Strategy 1: if *path* lives under a ``<prefix>/drive_X`` directory,
    map it to ``X:\\...`` (deterministic, no wine call).
    Strategy 2 (fallback): ask ``winepath -w``.
    The result must be absolute and SPACE-FREE for /config: (pitfall #2).
    """
    path = path.resolve()
    for parent in (path, *path.parents):
        m = re.fullmatch(r"drive_([A-Za-z])", parent.name)
        if m:
            rel = path.relative_to(parent)
            return f"{m.group(1).upper()}:\\{rel.as_posix().replace('/', chr(92))}"
    try:
        r = subprocess.run(
            ["winepath", "-w", str(path)],
            capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip().splitlines()[0]
    except (OSError, subprocess.TimeoutExpired):
        pass
    return str(path)  # last resort; caller validates


def _default_stage_dir() -> Optional[Path]:
    """Wine drive root derived from MT5_BASE (…/drive_c/… → drive_c).

    Matches the proven recipe: stage the INI at the drive root, e.g.
    ``C:/mts4.ini``.  Returns None if MT5_BASE is not under a drive_X.
    """
    for parent in (MT5_BASE, *MT5_BASE.parents):
        if re.fullmatch(r"drive_[A-Za-z]", parent.name):
            return parent
    return None


def _parse_ini_sections(text: str) -> dict[str, dict[str, str]]:
    """Parse INI text into {section: {key: value}} (comments skipped)."""
    sections: dict[str, dict[str, str]] = {}
    cur: Optional[dict[str, str]] = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            cur = sections.setdefault(line[1:-1].strip(), {})
            continue
        if cur is None or "=" not in line:
            continue
        k, _, v = line.partition("=")
        cur[k.strip()] = v.strip()
    return sections


def _validate_tester_inputs_lines(lines: list[str]) -> list[str]:
    """Return error strings for malformed [TesterInputs] lines (pitfall #5)."""
    errors: list[str] = []
    in_inputs = False
    for i, raw in enumerate(lines, 1):
        s = raw.strip()
        if s.lower().startswith("[testerinputs]"):
            in_inputs = True
            continue
        if s.startswith("["):
            in_inputs = False
            continue
        if not in_inputs or not s or s.startswith(";"):
            continue
        parts = s.split("||")
        if len(parts) != 5 or parts[4].strip().upper() not in ("Y", "N"):
            errors.append(
                f"  [TesterInputs] line {i}: {s!r} — must be "
                f"name=value||start||step||stop||Y|N"
            )
    return errors


def _resolve_expert_host(expert_value: str) -> Optional[Path]:
    """Resolve [Tester] Expert= to an existing .ex5 under host MQL5/Experts."""
    rel = expert_value.replace("\\", "/").lstrip("/")
    p = MQL5_DIR / "Experts" / rel
    if p.is_file():
        return p
    experts = MQL5_DIR / "Experts"
    if experts.is_dir():
        hits = sorted(experts.rglob(Path(rel).name))
        if hits:
            return hits[0]
    return None


def _validate_tester_ini(
    ini_path: Path, sections: dict[str, dict[str, str]]
) -> tuple[list[str], list[str]]:
    """Validate a tester INI. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    tester = sections.get("Tester")
    if tester is None:
        return (["  no [Tester] section found"], warnings)
    for key in _TESTER_REQUIRED_KEYS:
        if not tester.get(key):
            errors.append(f"  [Tester] missing required key: {key}")
    if tester.get("UseLocal") == "0":
        errors.append(
            "  [Tester] UseLocal=0 — no local agent will spawn and the run "
            "silently never starts; set UseLocal=1"
        )
    elif "UseLocal" not in tester:
        warnings.append("  [Tester] UseLocal missing — will be set to 1 in the staged copy")
    model = tester.get("Model", "0")
    if model not in MODEL_ENUM:
        errors.append(
            f"  [Tester] Model={model} unsupported (expected 0, 1, 2, 4: "
            + "; ".join(f"{k}={v}" for k, v in MODEL_ENUM.items()) + ")"
        )
    elif model == "4":
        warnings.append(
            "  Model=4 — every tick based on real ticks; falls back to generated "
            "ticks when the broker history has none (report's 'History Quality: "
            "0% real ticks' is the tell)"
        )
    optimization = tester.get("Optimization", "0")
    if optimization not in OPTIMIZATION_ENUM:
        errors.append(
            f"  [Tester] Optimization={optimization} invalid (expected 0-3: "
            + "; ".join(f"{k}={v}" for k, v in OPTIMIZATION_ENUM.items()) + ")"
        )
    expert = tester.get("Expert", "")
    if expert:
        host_ex5 = _resolve_expert_host(expert)
        if host_ex5 is None:
            errors.append(
                f"  [Tester] Expert={expert!r} — no such .ex5 under "
                f"{MQL5_DIR / 'Experts'} (deploy first: mql5_helper.py deploy)"
            )
    errors.extend(_validate_tester_inputs_lines(ini_path.read_text(
        encoding="utf-8-sig", errors="replace").splitlines()))
    return (errors, warnings)


def _normalize_tester_ini_text(
    lines: list[str], report_name: str
) -> list[str]:
    """Return normalized INI lines: forced keys + Report= (pitfall #4/#6/#8).

    Forces UseLocal=1, ReplaceReport=1, ShutdownTerminal=1 and
    Report=<report_name> in [Tester]. Missing Model/Optimization default
    to 0; explicit values and all other settings are kept verbatim.
    Caller converts to CRLF.
    """
    forced = {
        "UseLocal": "1",
        "ReplaceReport": "1",
        "ShutdownTerminal": "1",
        "Report": report_name,
    }
    defaults = {"Optimization": "0", "Model": "0"}
    present: set[str] = set()
    seen: set[str] = set()
    out: list[str] = []
    insert_at: Optional[int] = None  # index AFTER the last [Tester] line
    in_tester = False
    for raw in lines:
        s = raw.strip()
        if s.lower() == "[tester]":
            in_tester = True
        elif s.startswith("["):
            in_tester = False
        if in_tester and "=" in s and not s.startswith(";"):
            key = s.partition("=")[0].strip()
            present.add(key)
            if key in forced:
                if key not in seen:
                    seen.add(key)
                    out.append(f"{key}={forced[key]}")
                insert_at = len(out)
                continue
        out.append(raw.rstrip("\r\n"))
        if in_tester:
            insert_at = len(out)
    # Avoid inheriting a previous runner's optimization/model.
    forced.update({k: v for k, v in defaults.items() if k not in present})
    # Insert forced keys that were missing entirely (right after [Tester])
    missing = [k for k in forced if k not in seen]
    if missing:
        if insert_at is None:
            out.append("[Tester]")
            insert_at = len(out)
        for k in missing:
            out.insert(insert_at, f"{k}={forced[k]}")
            insert_at += 1
    return out


def _clone_ignore(directory, names):
    """shutil.copytree ignore fn: skip temp/logs and Tester agent caches."""
    d = Path(directory)
    ignored: set[str] = set()
    if d == MT5_BASE:
        ignored |= {"temp", "logs"}
    if d.name.lower() == "tester":
        ignored |= {
            n for n in names
            if n.startswith("Agent-") or n.lower() in ("cache", "logs")
        }
    return ignored


def _ensure_instance(instance: Path) -> None:
    """Bootstrap a runner instance by cloning MT5_BASE (pitfall #3)."""
    if (instance / "terminal64.exe").is_file():
        return
    print(f"Runner instance not found: {instance}")
    print(f"Cloning {MT5_BASE} → {instance}")
    print("  (Bases\\ can be several GB; temp/logs/Tester agent caches excluded)")
    shutil.copytree(MT5_BASE, instance, ignore=_clone_ignore, dirs_exist_ok=True)
    print("  clone done")


def _read_maybe_utf16(path: Path) -> str:
    """Read a log file, decoding UTF-16LE when BOM/NUL pattern present."""
    return _read_journal_since(path, 0)


def _read_journal_since(path: Path, byte_offset: int = 0) -> str:
    """Read a journal from *byte_offset*, returning text appended after it.

    UTF-16LE stores 2 bytes per character, so the byte offset is divided
    by 2 to get the character offset before slicing.
    """
    try:
        raw = path.read_bytes()
    except OSError:
        return ""
    if raw[:2] == b"\xff\xfe" or b"\x00" in raw[: min(len(raw), 1024)]:
        text = raw.decode("utf-16-le", errors="replace")
        return text[byte_offset // 2:]
    text = raw.decode("utf-8", errors="replace")
    return text[byte_offset:]


def _newest_journal(instance: Path, since: float) -> Optional[Path]:
    """Newest instance/logs/*.log modified after *since* (epoch sec)."""
    logs = instance / "logs"
    if not logs.is_dir():
        return None
    hits = [p for p in logs.glob("*.log") if p.stat().st_mtime >= since - 5]
    return max(hits, key=lambda p: p.stat().st_mtime) if hits else None


def _journal_key_lines(text: str) -> list[str]:
    """Extract the decision-relevant journal lines (pitfall #7)."""
    markers = (
        "automatic testing started",
        "last test passed",
        "automatic optimization started",
        "complete optimization started",
        "genetic optimization started",
        "optimization finished",
        "optimization done",
        "optimization stopped",
        "optimization cancelled",
        "new records saved to cache",
        "cannot load config",
        "exit with code",
        "no history",
        "tester agent",
    )
    return [
        ln.strip()
        for ln in text.splitlines()
        if any(m in ln for m in markers)
    ]


def _locate_report(
    instance: Path, report_name: str, since: float, *, optimization: bool = False
) -> Optional[Path]:
    """Find HTML (single test) or XML (optimization) in the instance root.

    Prefer the Report= stem, then MT5's ReportTester-/ReportOptimizer-
    fallback; never collect an unrelated file or a forward report.
    """
    def _newer(p: Path) -> bool:
        try:
            return p.stat().st_mtime >= since
        except OSError:
            return False

    suffixes = {".xml"} if optimization else {".htm", ".html"}
    stem = re.sub(r"\.(?:xml|html?)$", "", report_name, flags=re.IGNORECASE)
    cands = [p for p in instance.iterdir()
             if p.is_file() and p.suffix.lower() in suffixes and _newer(p)]
    named = [p for p in cands if p.stem == stem]
    prefix = "ReportOptimizer-" if optimization else "ReportTester-"
    pool = named or [p for p in cands if p.stem.lower().startswith(prefix.lower())
                     and not p.stem.lower().endswith('.forward')]
    return max(pool, key=lambda p: p.stat().st_mtime) if pool else None


def _kill_tree(popen: subprocess.Popen) -> None:
    """Terminate the detached terminal process group (POSIX: killpg)."""
    if IS_WINDOWS:
        popen.terminate()
        return
    try:
        os.killpg(os.getpgid(popen.pid), signal.SIGTERM)
    except (ProcessLookupError, PermissionError):
        return
    time.sleep(3)
    try:
        os.killpg(os.getpgid(popen.pid), signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        pass


def cmd_tester(args: argparse.Namespace) -> int:
    """Headless test/optimization: validate → stage → launch → poll → collect."""
    ini = Path(args.ini).resolve()
    if not ini.is_file():
        print(f"Error: INI not found: {ini}")
        return 1
    text = ini.read_text(encoding="utf-8-sig", errors="replace")
    sections = _parse_ini_sections(text)
    errors, warnings = _validate_tester_ini(ini, sections)
    for w in warnings:
        print(f"Warn:{w}")
    if errors:
        print("Error: INI validation failed:")
        print("\n".join(errors))
        return 1

    tester = sections["Tester"]
    optimization_mode = tester.get("Optimization", "0")
    optimization = optimization_mode != "0"
    print(f"Tester mode: {OPTIMIZATION_ENUM[optimization_mode]}")
    expert_rel = tester["Expert"].replace("\\", "/")
    host_ex5 = _resolve_expert_host(tester["Expert"])
    assert host_ex5 is not None  # validated above
    ea_stem = Path(expert_rel).stem
    ts = time.strftime("%Y%m%d-%H%M%S")
    report_name = args.report_name or f"{ea_stem}-{ts}"

    # --- runner instance (pitfall #3) ------------------------------------
    instance = (
        Path(args.instance).resolve() if args.instance
        else MT5_BASE.parent / "MetaTrader 5-auto"
    )
    terminal = instance / "terminal64.exe"
    if not IS_WINDOWS:
        if not shutil.which(args.wine):
            print(f"Error: wine binary not found: {args.wine}")
            return 1
    if not terminal.is_file() and args.dry_run:
        print(
            f"Dry run — instance {instance} missing; would be cloned from "
            f"{MT5_BASE} (skipped in dry run)."
        )
    else:
        _ensure_instance(instance)
        if not terminal.is_file():
            print(f"Error: terminal64.exe not found in instance: {terminal}")
            return 1

    # --- refresh the freshly-compiled .ex5 into the instance --------------
    if args.no_refresh:
        print("Skipping .ex5 refresh (--no-refresh)")
    elif args.dry_run and not terminal.is_file():
        print("Dry run — .ex5 refresh skipped (instance not bootstrapped)")
    else:
        inst_ex5 = instance / "MQL5" / "Experts" / expert_rel
        inst_ex5.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(host_ex5, inst_ex5)
        print(f"Refreshed .ex5: {host_ex5.name} → {inst_ex5}")

    # --- stage the normalized INI at a space-free Windows path -----------
    stage_dir = Path(args.stage_dir).resolve() if args.stage_dir else _default_stage_dir()
    if stage_dir is None:
        print(
            "Error: cannot derive a stage directory (MT5_BASE is not under a "
            "Wine drive_X). Pass --stage-dir DIR pointing inside the Wine "
            "C: drive, e.g. <prefix>/drive_c/tmp"
        )
        return 1
    stage_dir.mkdir(parents=True, exist_ok=True)
    staged = stage_dir / f"tester-{ea_stem.replace(' ', '_')}-{ts}.ini"
    norm_lines = _normalize_tester_ini_text(
        text.splitlines(), report_name
    )
    staged.write_bytes(("\r\n".join(norm_lines) + "\r\n").encode("utf-8"))
    win_cfg = _posix_to_win(staged)
    if " " in win_cfg:
        print(
            f"Error: staged config path contains spaces: {win_cfg}\n"
            "  MT5 cannot load a /config: path with spaces even when quoted "
            "(pitfall #2). Re-run with --stage-dir pointing at a space-free "
            "location inside a Wine drive, e.g. <prefix>/drive_c"
        )
        return 1
    print(f"Staged INI: {staged}  (as {win_cfg})")

    # --- launch command ---------------------------------------------------
    if IS_WINDOWS:
        cmd = [str(terminal), "/portable", f"/config:{win_cfg}"]
    else:
        cmd = [args.wine, str(terminal), "/portable", f"/config:{win_cfg}"]
    print(f"Launch: {' '.join(cmd)}")
    print(f"Working dir (report lands here, pitfall #1): {instance}")
    if args.dry_run:
        print("Dry run — stopping before launch.")
        return 0

    # --- launch detached (pitfall #6) -------------------------------------
    # Snapshot BEFORE launch so fast runs cannot hide their first journal lines.
    t_launch = time.time()
    base_jp = _newest_journal(instance, t_launch - 86400)
    base_jp_name = base_jp.name if base_jp else None
    base_offset = base_jp.stat().st_size if base_jp else 0
    # Optimization completion is in tester/logs, not terminal logs.
    tester_log_dirs = [instance / "tester" / "logs", instance / "Tester" / "logs"]
    tester_offsets = {
        p: p.stat().st_size
        for d in tester_log_dirs for p in d.glob("*.log")
    }
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=str(instance),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=not IS_WINDOWS,
        )
    except OSError as e:
        print(f"Error: launch failed: {e}")
        return 1
    print(f"Launched pid={proc.pid}; polling (timeout {args.timeout}s) …")

    status = "timeout"
    seen_events: set[str] = set()
    journal_path: Optional[Path] = None
    # Journal baseline: logs/YYYYMMDD.log is CUMULATIVE for the day, so a
    # naive full-file grep sees this morning's stale `cannot load config`
    # lines and aborts a healthy launch. Only content appended after the
    # launch (bytes past the baseline offset, or a newly-created file)
    # counts as evidence.
    try:
        deadline = t_launch + args.timeout
        while time.time() < deadline:
            if proc.poll() is not None:
                status = "exited"
                break
            time.sleep(2)
            jp = _newest_journal(instance, t_launch)
            if jp is not None:
                jtext = _read_journal_since(jp, base_offset if jp.name == base_jp_name else 0)
                if "cannot load config" in jtext and "config-load-error" not in seen_events:
                    seen_events.add("config-load-error")
                    print("FAIL: journal reports 'cannot load config' — aborting (pitfall #2)")
                    _kill_tree(proc)
                    status = "config-load-error"
                    journal_path = jp
                    break
                if "automatic testing started" in jtext and "started" not in seen_events:
                    seen_events.add("started")
                    print("Journal: automatic testing started")
                journal_path = jp
        else:
            print(f"Timeout after {args.timeout}s — killing terminal")
            _kill_tree(proc)
    except KeyboardInterrupt:
        print("\nInterrupted — killing terminal")
        _kill_tree(proc)
        return 130

    # --- post-mortem: journal + report ------------------------------------
    time.sleep(1.5)
    if journal_path is None:
        journal_path = _newest_journal(instance, t_launch)
    key_lines: list[str] = []
    if journal_path is not None:
        jtext = _read_journal_since(
            journal_path, base_offset if journal_path.name == base_jp_name else 0
        )
        key_lines = _journal_key_lines(jtext)
        print(f"\nJournal: {journal_path}")
        for ln in key_lines:
            print(f"  {ln}")
    else:
        print(f"\nWarn: no journal found under {instance / 'logs'}")

    tester_journals: list[str] = []
    optimization_lines: list[str] = []
    if optimization:
        for jp in sorted({p for d in tester_log_dirs for p in d.glob("*.log")}):
            new_text = _read_journal_since(jp, tester_offsets.get(jp, 0))
            if not new_text:
                continue
            tester_journals.append(str(jp))
            lines = _journal_key_lines(new_text)
            optimization_lines.extend(lines)
            print(f"\nTester journal: {jp}")
            for ln in lines:
                print(f"  {ln}")
        key_lines.extend(optimization_lines)
        passed = any(re.search(r"optimization finished, total passes [1-9]\d*\b", ln)
                     for ln in optimization_lines)
        passed = passed and not any(
            marker in ln for ln in optimization_lines
            for marker in ("optimization stopped", "optimization cancelled")
        )
    else:
        passed = any('last test passed with result "successfully finished"' in ln
                     for ln in key_lines)
    report = _locate_report(instance, report_name, t_launch, optimization=optimization)

    outdir = (
        Path(args.out).resolve() if args.out
        else Path.cwd() / f"tester-report-{ea_stem}-{ts}"
    )
    artifacts: list[str] = []
    if report is not None:
        outdir.mkdir(parents=True, exist_ok=True)
        to_copy = [report] + [
            p for suf in _REPORT_PNG_SUFFIXES
            for p in [instance / f"{report.stem}{suf}"] if not optimization and p.is_file()
        ]
        for p in to_copy:
            dest = outdir / p.name
            shutil.copy2(p, dest)
            artifacts.append(str(dest))
        print(f"\nReport: {report.name} → {outdir}")
    elif status == "exited":
        print(
            f"\nError: no report found in {instance} newer than launch "
            f"(pitfall #1 — Report= lands in the terminal working dir)"
        )

    if args.json:
        print(json.dumps({
            "status": status,
            "passed": passed,
            "ea": expert_rel,
            "optimization": optimization_mode,
            "instance": str(instance),
            "staged_ini": str(staged),
            "journal": str(journal_path) if journal_path else None,
            "journal_key_lines": key_lines,
            "tester_journals": tester_journals,
            "report": str(report) if report else None,
            "outdir": str(outdir) if artifacts else None,
            "artifacts": artifacts,
            "elapsed_s": round(time.time() - t_launch, 1),
        }, indent=2))
    elif passed and artifacts and not args.no_summary:
        # XML optimization vs HTML single-test summary (same interpreter).
        parser = Path(__file__).with_name(
            "parse_optimizer_report.py" if optimization else "parse_tester_report.py"
        )
        try:
            r = subprocess.run(
                [sys.executable, str(parser), "report", str(outdir / report.name)],
                timeout=120,
            )
            if r.returncode != 0:
                print(
                    "\nWarn: summary parser failed — open the report manually: "
                    f"{outdir / report.name}"
                )
        except (OSError, subprocess.TimeoutExpired):
            print(f"\nNote: parse the report with: {parser.name} report {outdir / report.name}")

    if status == "timeout":
        return 2
    if status != "exited":
        return 1
    if not passed:
        return 1
    if report is None:
        return 1
    print("\nTester OK.")
    return 0


# ---------------------------------------------------------------------------
# init-ini — generate a [Tester]/[TesterInputs] skeleton from .mq5 inputs
# ---------------------------------------------------------------------------

_INPUT_RE = re.compile(
    r"^\s*(s?input)\s+([A-Za-z_]\w*)\s+([A-Za-z_]\w*)\s*=\s*(.*)$"
)
_GROUP_RE = re.compile(r'^\s*input\s+group\s+(.+?)\s*$')

_INT_TYPES = {"int", "uint", "long", "ulong", "short", "ushort", "char", "uchar"}


def _cut_value(rest: str) -> tuple[str, str]:
    """Split ``value; // comment`` respecting quotes. Returns (value, comment)."""
    q: Optional[str] = None
    end: Optional[int] = None
    i = 0
    while i < len(rest):
        ch = rest[i]
        if q:
            if ch == q:
                q = None
        elif ch in "'\"":
            q = ch
        elif ch == ";":
            end = i
            break
        elif ch == "/" and rest[i:i + 2] == "//":
            end = i
            break
        i += 1
    if end is None:
        value, tail = rest, ""
    else:
        value, tail = rest[:end], rest[end:]
    cmt = ""
    idx = tail.find("//")
    if idx >= 0:
        cmt = tail[idx + 2:].strip()
    return value.strip(), cmt


def _ini_value_step(typ: str, value: str) -> tuple[str, str, bool]:
    """Return (ini_value, step, needs_manual_check) for an input default.

    Step convention (SKILL.md §6 / pitfall #5): booleans and enums use
    step=0 (only start/stop matter); doubles 0.1; ints 1. Enum/color
    identifiers can't be resolved from source — kept verbatim + flagged.
    """
    v = value.strip()
    m = re.fullmatch(r"[Dd]'([^']*)'", v)
    if m:
        # D'yyyy.mm.dd' → MT5 INI expects the plain date text
        return m.group(1), "0", False
    t = typ.lower()
    if t == "bool":
        return v.lower(), "0", False
    if t == "string":
        return v.strip('"'), "0", False
    if t in ("double", "float"):
        return v, "0.1", not re.fullmatch(r"-?\d+(\.\d+)?", v)
    if t in _INT_TYPES:
        return v, "1", not re.fullmatch(r"-?\d+", v)
    # enum / color / datetime / other identifiers
    return v, "0", not re.fullmatch(r"-?\d+", v)


def _scan_mq5_inputs(src: Path) -> list[dict]:
    """Extract every input/sinput declaration from an .mq5 source."""
    try:
        text = src.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"Error: cannot read {src}: {e}")
        sys.exit(1)
    inputs: list[dict] = []
    group: Optional[str] = None
    for ln, raw in enumerate(text.splitlines(), 1):
        g = _GROUP_RE.match(raw)
        if g:
            group = g.group(1).strip().strip('"')
            continue
        m = _INPUT_RE.match(raw)
        if not m:
            continue
        kw, typ, name, rest = m.groups()
        value, comment = _cut_value(rest)
        ini_value, step, todo = _ini_value_step(typ, value)
        inputs.append({
            "name": name,
            "type": typ,
            "value": ini_value,
            "step": step,
            "comment": comment,
            "group": group,
            "sinput": kw == "sinput",
            "todo": todo,
            "line": ln,
        })
    return inputs


def cmd_init_ini(args: argparse.Namespace) -> int:
    """Generate a Tester INI skeleton listing ALL inputs of an .mq5."""
    src = Path(args.file).resolve()
    if not src.is_file():
        print(f"Error: {src} not found")
        return 1
    inputs = _scan_mq5_inputs(src)
    if not inputs:
        print(f"Error: no input declarations found in {src.name}")
        return 1

    if args.json:
        print(json.dumps(inputs, indent=2))
        return 0

    ea_stem = src.stem
    today = date.today()
    date_from = args.date_from or (today - timedelta(days=730)).strftime("%Y.%m.%d")
    date_to = args.date_to or today.strftime("%Y.%m.%d")
    report = args.report or f"{ea_stem}"
    expert = args.expert or f"{ea_stem}.ex5"

    out = Path(args.out).resolve() if args.out else src.with_suffix(".ini")
    if out.exists() and not args.force:
        print(f"Error: output exists: {out} (use --force to overwrite)")
        return 1

    lines = [
        f"; Generated by mql5_helper.py init-ini from {src.name} "
        f"at {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "; Every input is listed as name=value||start||step||stop||Y|N —",
        "; inputs OMITTED from [TesterInputs] silently fall back to EA source",
        "; defaults (GIGO trap). To optimize a parameter: set start/step/stop",
        "; and flip the trailing N → Y, then set Optimization=1 for complete Grid.",
        "",
        "[Tester]",
        f"Expert={expert}",
        f"Symbol={args.symbol}",
        f"Period={args.period}",
        "Optimization=0",
        f"Model={args.model}",
        f"FromDate={date_from}",
        f"ToDate={date_to}",
        "ForwardMode=0",
        f"Deposit={args.deposit}",
        f"Currency={args.currency}",
        "ProfitInPips=0",
        f"Leverage={args.leverage}",
        "ExecutionMode=500",
        "OptimizationCriterion=1",
        f"Report={report}",
        "ReplaceReport=1",
        "UseLocal=1",
        "ShutdownTerminal=1",
        "",
        "[TesterInputs]",
    ]
    cur_group: Optional[str] = None
    todos = 0
    for inp in inputs:
        if inp["group"] != cur_group:
            cur_group = inp["group"]
            if cur_group:
                lines.append(f"; --- {cur_group} ---")
        if inp["comment"]:
            lines.append(f"; {inp['comment']}")
        val, step = inp["value"], inp["step"]
        lines.append(
            f"{inp['name']}={val}||{val}||{step}||{val}||N"
        )
        if inp["todo"]:
            todos += 1
            lines.append(
                f"; TODO: {inp['name']} ({inp['type']}) — value {val!r} is an "
                "identifier; replace with the numeric enum/datetime value"
            )
        if inp["sinput"]:
            lines.append(f"; note: {inp['name']} is sinput — never optimizable")
    out.write_bytes(("\r\n".join(lines) + "\r\n").encode("utf-8"))

    print(f"Inputs parsed: {len(inputs)}  →  {out}")
    if todos:
        print(
            f"Warn: {todos} value(s) are enum/datetime identifiers — replace "
            "them with numeric values before running (see TODO comments)"
        )
    print("Next: review Symbol/Period/dates/Optimization, then run: mql5_helper.py tester " + str(out))
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="MQL5 development helper (compile, check, deploy)"
    )
    # Global option — must be parsed before subcommand so we can apply .env
    # before resolving MT5_BASE / MQL5_DIR.  When omitted, the script walks
    # up from cwd looking for the project-root ``.env`` (the default).
    parser.add_argument(
        "--env-file",
        type=Path,
        metavar="PATH",
        help="Explicit .env file (overrides walk-up search for .env).",
    )
    parser.add_argument(
        "--no-env",
        action="store_true",
        help="Skip .env loading entirely; rely on env vars only.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show MT5 installation status")
    sub.add_parser("list", help="List MQ5 source files in MQL5 directory")

    compile_p = sub.add_parser("compile", help="Compile MQ5 → EX5")
    compile_p.add_argument("file", help="Path to .mq5 file")

    check_p = sub.add_parser("check", help="Syntax-check only (no .ex5 output)")
    check_p.add_argument("file", help="Path to .mq5 file")

    deploy_p = sub.add_parser("deploy", help="Compile .mq5 then deploy .ex5 to MQL5 tree")
    deploy_p.add_argument("file", help="Path to .mq5 file")

    init_p = sub.add_parser(
        "init-ini",
        help="Generate a [Tester]/[TesterInputs] INI skeleton from .mq5 inputs",
    )
    init_p.add_argument("file", help="Path to .mq5 source")
    init_p.add_argument("-o", "--out", metavar="FILE", help="Output .ini (default: <source>.ini)")
    init_p.add_argument("--expert", help="[Tester] Expert= value (default: <stem>.ex5)")
    init_p.add_argument("--symbol", default="XAUUSD")
    init_p.add_argument("--period", default="M15")
    init_p.add_argument("--from", dest="date_from", metavar="YYYY.MM.DD",
                        help="FromDate (default: today-2y)")
    init_p.add_argument("--to", dest="date_to", metavar="YYYY.MM.DD",
                        help="ToDate (default: today)")
    init_p.add_argument("--model", choices=MODEL_ENUM, default="4",
                        help="0=every tick, 1=M1 OHLC, 2=open prices, 4=real ticks (default)")
    init_p.add_argument("--deposit", default="10000")
    init_p.add_argument("--currency", default="USD")
    init_p.add_argument("--leverage", default="100")
    init_p.add_argument("--report", help="[Tester] Report= base name (default: <stem>)")
    init_p.add_argument("--force", action="store_true", help="Overwrite existing output")
    init_p.add_argument("--json", action="store_true", help="Print parsed inputs as JSON, no INI")

    bt = sub.add_parser(
        "tester",
        help="Headless single test or Grid optimization via INI: terminal64.exe /portable /config:<INI>",
    )
    bt.add_argument("ini", help="Tester config .ini (format: references/quick-ref-tester-automation.md)")
    bt.add_argument("--instance", metavar="DIR",
                    help="Runner clone dir (default: <MT5_BASE parent>/MetaTrader 5-auto; "
                         "bootstrapped by cloning MT5_BASE if missing)")
    bt.add_argument("--no-refresh", action="store_true",
                    help="Skip copying the EA .ex5 from host MQL5 into the instance")
    bt.add_argument("--stage-dir", metavar="DIR",
                    help="Dir to stage the normalized INI (default: Wine drive root derived "
                         "from MT5_BASE, e.g. drive_c → C:\\). Must yield a SPACE-FREE "
                         "Windows path (pitfall #2)")
    bt.add_argument("-o", "--out", metavar="DIR",
                    help="Dir to receive single-test HTML + PNGs or optimization XML "
                         "(default: ./tester-report-<EA>-<ts>)")
    bt.add_argument("--report-name", help="Override [Tester] Report= base name")
    bt.add_argument("--timeout", type=int, default=3600, help="Seconds (default 3600)")
    bt.add_argument("--wine", default="wine", help="Wine binary (Unix only)")
    bt.add_argument("--dry-run", action="store_true",
                    help="Validate, stage, prepare, print launch command; do NOT launch")
    bt.add_argument("--json", action="store_true", help="Emit result as JSON")
    bt.add_argument("--no-summary", action="store_true",
                    help="Skip the single-test/optimization report summary print")

    args = parser.parse_args(argv)

    # Resolve paths (.env loading + auto-detection) before any command runs
    if args.no_env:
        global MT5_BASE, MQL5_DIR
        MT5_BASE, MQL5_DIR = _resolve_paths()
    else:
        _apply_paths(args.env_file)

    commands = {
        "status": cmd_status,
        "list": cmd_list,
        "compile": cmd_compile,
        "check": cmd_check,
        "deploy": cmd_deploy,
        "init-ini": cmd_init_ini,
        "tester": cmd_tester,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
