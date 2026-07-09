#!/usr/bin/env python3
"""
MQL5 development helper: compile, check, deploy, list, status.

Supports Windows 10+ natively (PowerShell) and Linux/Wine.

Usage:
    python skills/mql5/scripts/mql5_helper.py compile FILE.mq5
    python skills/mql5/scripts/mql5_helper.py check FILE.mq5
    python skills/mql5/scripts/mql5_helper.py deploy FILE.mq5
    python skills/mql5/scripts/mql5_helper.py status
    python skills/mql5/scripts/mql5_helper.py list
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# MetaEditor/terminal executables with priority scores (higher=better)
_MT5_MARKERS: tuple[tuple[str, int], ...] = (
    ("MetaEditor64.exe", 2),  # needed for compile
    ("metaeditor64.exe", 1),
    ("terminal64.exe", 0),
    ("terminal.exe", 0),
)

_MQL5_MARKERS = ("Experts", "Indicators", "Scripts")

TYPE_DIRS: dict[str, str] = {
    "expert": "Experts",
    "indicator": "Indicators",
    "script": "Scripts",
    "service": "Services",
    "include": "Include",
}

IS_WINDOWS = sys.platform == "win32"

def _load_env(env_path: Optional[Path] = None) -> None:
    """Load MT5_BASE / MQL5_DIR from a .env file.

    *env_path* — optional explicit path.  When given, that file must
    exist (raises ``SystemExit(1)`` on missing).  When ``None`` (the
    default), walks up from ``Path.cwd()`` and uses the first
    ``.hermes/.env`` it finds (silent on miss — pre-existing behaviour).

    Supports ``KEY="VALUE" KEY2="VALUE2"`` on one line (space-separated),
    one-var-per-line, or mixes thereof, using ``shlex.split`` for quoting.
    """
    if env_path is not None:
        env_path = Path(env_path)
        if not env_path.is_file():
            print(f"Error: --env-file not found: {env_path}")
            sys.exit(1)
        candidates: list[Path] = [env_path]
    else:
        candidates = []
        d = Path.cwd()
        while True:
            ef = d / ".hermes" / ".env"
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
            if key in ("MT5_BASE", "MQL5_DIR"):
                os.environ.setdefault(key, val)


# ---------------------------------------------------------------------------
# Path resolution  ($MT5_BASE / $MQL5_DIR → cwd walk-up → Program Files →
#                    Wine fallback)
# ---------------------------------------------------------------------------


def _find_mt5_in_program_files() -> Optional[Path]:
    """Scan Program Files directories for a MetaTrader 5 installation.

    On Windows scans native ``C:\\Program Files`` and
    ``C:\\Program Files (x86)``.  On Linux/Wine scans under ``/`` and
    ``~`` equivalents.
    """
    candidates: list[Path] = []
    if IS_WINDOWS:
        candidates = [
            Path("C:/Program Files"),
            Path("C:/Program Files (x86)"),
        ]
    else:
        for root in (Path("/"), Path.home()):
            for name in ("Program Files", "Program Files (x86)"):
                candidates.append(root / name)

    found: list[tuple[int, Path]] = []
    for pf in candidates:
        if not pf.is_dir():
            continue
        try:
            entries = list(pf.iterdir())
        except PermissionError:
            continue
        for d in entries:
            if not d.is_dir():
                continue
            score = -1
            for exe, s in _MT5_MARKERS:
                if (d / exe).exists():
                    score = max(score, s)
            if score >= 0:
                found.append((score, d))
    if not found:
        return None
    found.sort(key=lambda t: t[0], reverse=True)
    return found[0][1]


def _detect_mql5_from_cwd() -> Optional[Path]:
    """Walk up from cwd; return first dir with ≥2 MQL5 marker subdirs."""
    d = Path.cwd()
    while True:
        hits = sum(1 for m in _MQL5_MARKERS if (d / m).is_dir())
        if hits >= 2:
            return d
        parent = d.parent
        if parent == d:
            return None
        d = parent


def _resolve_paths() -> tuple[Path, Path]:
    """Return (MT5_BASE, MQL5_DIR) using the priority chain.

    MT5_BASE priority:  env var → Program Files scan → Wine fallback.
    MQL5_DIR priority:  env var → cwd walk-up → MT5_BASE / "MQL5".
    """
    # -- MT5_BASE --
    if "MT5_BASE" in os.environ:
        mt5_base = Path(os.environ["MT5_BASE"])
    else:
        found = _find_mt5_in_program_files()
        if found is not None:
            mt5_base = found
        elif IS_WINDOWS:
            print("Error: MetaTrader 5 not found. Set MT5_BASE in .hermes/.env")
            sys.exit(1)
        else:
            mt5_base = Path.home() / ".wine/drive_c/Program Files/MetaTrader 5"

    # -- MQL5_DIR --
    if "MQL5_DIR" in os.environ:
        mql5_dir = Path(os.environ["MQL5_DIR"])
    else:
        detected = _detect_mql5_from_cwd()
        if detected is not None:
            mql5_dir = detected
            if "MT5_BASE" not in os.environ:
                # Implicit: MT5 is one level above the MQL5 dir found by cwd walk
                mt5_base = mql5_dir.parent
        else:
            mql5_dir = mt5_base / "MQL5"
    return mt5_base, mql5_dir


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
    On Wine: convert to Windows drive-letter style (``X:\\...``).
    """
    if IS_WINDOWS:
        return str(path)
    # Wine path conversion
    wine_prefix = Path(os.environ.get("WINEPREFIX", Path.home() / ".wine"))
    for letter in "cdefgh":
        drive_dir = wine_prefix / f"drive_{letter}"
        if not drive_dir.is_dir():
            continue
        try:
            rel = path.relative_to(drive_dir)
            rel_str = rel.as_posix().replace("/", "\\")
            return f"{letter.upper()}:\\{rel_str}"
        except ValueError:
            continue
    return str(path)


def _build_editor_cmd(editor: Path, flags: list[str]) -> list[str]:
    """Return ``subprocess.run`` command args for the target platform."""
    if IS_WINDOWS:
        return [str(editor), *flags]
    return ["wine", str(editor), *flags]


# ---------------------------------------------------------------------------
# Type detection (path-only, no content read)
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
            print(f"  ✓ {ex5_path.name}  ({ex5_path.stat().st_mtime - t_before:.1f}s after start)")
        else:
            what = "not found" if not ex5_path.exists() else "stale (mtime before compile)"
            issues.append(f"  ✗ {ex5_path.name} — {what}")

    if log_path.exists() and log_path.stat().st_mtime > t_before:
        elapsed = time.time() - log_path.stat().st_mtime
        print(f"  ✓ {log_path.name}  ({log_path.stat().st_mtime - t_before:.1f}s after start)")
    else:
        what = "not found" if not log_path.exists() else "stale (mtime before compile)"
        issues.append(f"  ✗ {log_path.name} — {what}")

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
# Core: deploy + run editor + freshness check
# ---------------------------------------------------------------------------


def _run_editor(src: Path, extra_flags: list[str], *, expect_ex5: bool) -> int:
    """Deploy *src* to MQL5 dir, invoke MetaEditor, verify freshness.

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

    # Deploy to MQL5 tree
    ptype = detect_type(src)
    dest_dir = MQL5_DIR / TYPE_DIRS.get(ptype, "Experts")
    dest = dest_dir / src.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Deployed: {src.name} → {dest}")

    # Pre-remove stale outputs so they can't fake freshness
    t_before = time.time()
    ex5_path = dest.with_suffix(".ex5")
    log_path = dest.with_suffix(".log")
    for p in (ex5_path, log_path):
        if p.exists():
            p.unlink()

    # Build command
    compile_arg = f'/compile:"{_to_editor_path(dest)}"'
    cmd = _build_editor_cmd(editor, [compile_arg, "/log", *extra_flags])

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
    return result.returncode


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
    """Deploy an MQ5 file to the MQL5 directory tree."""
    src = Path(args.file).resolve()
    if not src.is_file():
        print(f"Error: {src} not found")
        return 1
    ptype = detect_type(src)
    dest_dir = MQL5_DIR / TYPE_DIRS.get(ptype, "Experts")
    dest = dest_dir / src.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Deployed: {src.name} → {dest}")
    print(f"Type: {ptype}")
    print("Compile in MetaEditor or via: mql5_helper.py compile FILE.mq5")
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
        print(f'    & "{editor or MT5_BASE / "MetaEditor64.exe"}" /compile:"path\to\file.mq5" /log')
    else:
        print(f"  Wine compile template:")
        print(f'    wine "{editor or MT5_BASE / "MetaEditor64.exe"}" /compile:"Z:\\path\\to\\file.mq5" /log')
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
# CLI entry point
# ---------------------------------------------------------------------------


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="MQL5 development helper (compile, check, deploy)"
    )
    # Global option — must be parsed before subcommand so we can apply .env
    # before resolving MT5_BASE / MQL5_DIR.  When omitted, the script walks
    # up from cwd looking for ``.hermes/.env`` (the default behaviour).
    parser.add_argument(
        "--env-file",
        type=Path,
        metavar="PATH",
        help="Explicit .env file (overrides walk-up search for .hermes/.env).",
    )
    parser.add_argument(
        "--no-env",
        action="store_true",
        help="Skip .env loading entirely; rely on env vars + auto-detection.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show MT5 installation status")
    sub.add_parser("list", help="List MQ5 source files in MQL5 directory")

    compile_p = sub.add_parser("compile", help="Compile MQ5 → EX5")
    compile_p.add_argument("file", help="Path to .mq5 file")

    check_p = sub.add_parser("check", help="Syntax-check only (no .ex5 output)")
    check_p.add_argument("file", help="Path to .mq5 file")

    deploy_p = sub.add_parser("deploy", help="Copy .mq5 to the MQL5 directory tree")
    deploy_p.add_argument("file", help="Path to .mq5 file")

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
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
