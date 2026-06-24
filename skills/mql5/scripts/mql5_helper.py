#!/usr/bin/env python3
"""
MQL5 development helper: compile, check, deploy, and list EA/Indicator files.

CLI-automatable tasks only. Backtesting and optimization are GUI-only
(Strategy Tester).

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
from pathlib import Path

# MT5 paths — override via env vars if not default locations
#   MT5_BASE: MetaEditor/terminal install dir (default: Wine path)
#   MQL5_DIR: MQL5 data dir (default: MT5_BASE/MQL5, correct for Linux/Wine;
#             on Windows 10+ it's %APPDATA%\MetaQuotes\Terminal\<hex>\MQL5)
MT5_BASE = Path(os.environ.get("MT5_BASE", Path.home() / ".wine/drive_c/Program Files/MetaTrader 5"))
MQL5_DIR = Path(os.environ.get("MQL5_DIR", MT5_BASE / "MQL5"))

# Type → directory mapping
TYPE_DIRS = {
    "expert": "Experts",
    "indicator": "Indicators",
    "script": "Scripts",
    "service": "Services",
    "include": "Include",
}


def detect_type(file_path: Path) -> str:
    """Detect program type from file path segments (path-only, no content read)."""
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
    return "expert"  # default


def _find_editor() -> Path | None:
    """Locate MetaEditor64.exe / MetaEditor.exe in MT5 installation."""
    candidates = [
        MT5_BASE / "MetaEditor64.exe",
        MT5_BASE / "MetaEditor.exe",
    ]
    for p in MT5_BASE.rglob("MetaEditor*.exe"):
        candidates.append(p)
    for c in candidates:
        if c.exists():
            return c
    return None


def cmd_compile(args):
    """Compile an MQ5 file using MetaEditor via Wine.

    Deploys the file to the MQL5 directory first, then compiles.
    Generates a .log file alongside the source.
    """
    src = Path(args.file).resolve()
    if not src.exists():
        print(f"Error: {src} not found")
        return 1

    editor = _find_editor()
    if not editor:
        print("Error: MetaEditor.exe not found in MT5 installation")
        print(f"Searched: {MT5_BASE}")
        return 1

    # Deploy to MQL5 tree
    program_type = detect_type(src)
    dest_dir = MQL5_DIR / TYPE_DIRS.get(program_type, "Experts")
    dest = dest_dir / src.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Deployed: {src.name} → {dest}")

    # Compile: /compile:"path" /log (absolute path, cwd doesn't matter)
    try:
        result = subprocess.run(
            ["wine", str(editor), f'/compile:"{dest}"', "/log"],
            capture_output=True, text=True, timeout=60,
            cwd=str(dest.parent),
        )
        print(f"Compile output:\n{result.stdout}")
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")
        # Check for .log file
        log_path = dest.with_suffix(".log")
        if log_path.exists():
            log_text = log_path.read_text(errors="replace")
            # Print last 30 lines of log for quick review
            lines = log_text.strip().splitlines()
            if lines:
                print(f"\nCompilation log ({len(lines)} lines):")
                for line in lines[-30:]:
                    print(f"  {line}")
        return result.returncode
    except FileNotFoundError:
        print("Error: wine not found. Install wine first.")
        return 1
    except subprocess.TimeoutExpired:
        print("Compile timed out (60s). Check MetaEditor for errors.")
        return 1


def cmd_check(args):
    """Syntax-check an MQ5 file without full compilation (/s flag).

    Deploys the file to the MQL5 directory first, then runs syntax check.
    Generates a .log file alongside the source.
    """
    src = Path(args.file).resolve()
    if not src.exists():
        print(f"Error: {src} not found")
        return 1

    editor = _find_editor()
    if not editor:
        print("Error: MetaEditor.exe not found in MT5 installation")
        print(f"Searched: {MT5_BASE}")
        return 1

    # Deploy to MQL5 tree
    program_type = detect_type(src)
    dest_dir = MQL5_DIR / TYPE_DIRS.get(program_type, "Experts")
    dest = dest_dir / src.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Deployed: {src.name} → {dest}")

    # Syntax check: /compile:"path" /log /s (absolute path)
    try:
        result = subprocess.run(
            ["wine", str(editor), f'/compile:"{dest}"', "/log", "/s"],
            capture_output=True, text=True, timeout=60,
            cwd=str(dest.parent),
        )
        print(f"Syntax check output:\n{result.stdout}")
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")
        # Check for .log file
        log_path = dest.with_suffix(".log")
        if log_path.exists():
            log_text = log_path.read_text(errors="replace")
            lines = log_text.strip().splitlines()
            if lines:
                print(f"\nSyntax check log ({len(lines)} lines):")
                for line in lines[-30:]:
                    print(f"  {line}")
        return result.returncode
    except FileNotFoundError:
        print("Error: wine not found. Install wine first.")
        return 1
    except subprocess.TimeoutExpired:
        print("Syntax check timed out (60s).")
        return 1


def cmd_deploy(args):
    """Deploy an MQ5 file to the correct MQL5 directory."""
    src = Path(args.file).resolve()
    if not src.exists():
        print(f"Error: {src} not found")
        return 1

    program_type = detect_type(src)
    dest_dir = MQL5_DIR / TYPE_DIRS.get(program_type, "Experts")
    dest = dest_dir / src.name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Deployed: {src.name} → {dest}")
    print(f"Type: {program_type}")
    print("Compile in MetaEditor or via: mql5_helper.py compile FILE.mq5")
    return 0


def cmd_status(args):
    """Show MT5 installation status."""
    print(f"MT5 Base:    {MT5_BASE}")
    print(f"MQL5 Dir:    {MQL5_DIR}")
    print(f"Exists:      {MQL5_DIR.exists()}")

    if MQL5_DIR.exists():
        for subdir in ["Experts", "Indicators", "Scripts", "Services", "Include"]:
            d = MQL5_DIR / subdir
            if d.exists():
                mq5 = list(d.rglob("*.mq5"))
                ex5 = list(d.rglob("*.ex5"))
                print(f"  {subdir:12s}: {len(mq5)} .mq5, {len(ex5)} .ex5")

    print(f"\nTerminal:    {MT5_BASE / 'terminal64.exe'}")
    print(f"  Exists:    {(MT5_BASE / 'terminal64.exe').exists()}")
    return 0


def cmd_list(args):
    """List all MQ5 source files in MQL5 directory."""
    if not MQL5_DIR.exists():
        print("MQL5 directory not found")
        return 1

    for subdir in ["Experts", "Indicators", "Scripts", "Services"]:
        d = MQL5_DIR / subdir
        if not d.exists():
            continue
        files = sorted(d.rglob("*.mq5"))
        if files:
            print(f"\n{subdir}/")
            for f in files:
                rel = f.relative_to(d)
                print(f"  {rel}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="MQL5 development helper (compile, check, deploy)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show MT5 installation status")
    sub.add_parser("list", help="List all MQ5 source files")

    compile_p = sub.add_parser("compile", help="Compile an MQ5 file")
    compile_p.add_argument("file", help="Path to .mq5 file")

    check_p = sub.add_parser("check", help="Syntax-check an MQ5 file (no .ex5 output)")
    check_p.add_argument("file", help="Path to .mq5 file")

    deploy_p = sub.add_parser("deploy", help="Deploy MQ5 to MQL5 directory")
    deploy_p.add_argument("file", help="Path to .mq5 file")

    args = parser.parse_args()

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
