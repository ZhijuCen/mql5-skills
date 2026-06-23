#!/usr/bin/env python3
"""
MQL5 development helper: compile, deploy, and manage EA/Indicator files.

Usage:
    python skills/mql5/scripts/mql5_helper.py compile FILE.mq5
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

# Default MT5 paths
MT5_BASE = Path.home() / ".wine/drive_c/Program Files/MetaTrader 5"
MQL5_DIR = MT5_BASE / "MQL5"

# Type → directory mapping
TYPE_DIRS = {
    "expert": "Experts",
    "indicator": "Indicators",
    "script": "Scripts",
    "service": "Services",
    "include": "Include",
}


def detect_type(file_path: Path) -> str:
    """Detect program type from file path or content."""
    parts = file_path.parts
    for p in parts:
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

    # Detect from content
    try:
        content = file_path.read_text(errors="ignore")[:2000]
        if "OnTick()" in content or "OnTester()" in content:
            return "expert"
        if "OnCalculate(" in content:
            return "indicator"
        if "OnStart()" in content:
            return "script"
    except Exception:
        pass

    return "expert"  # default


def get_dest_dir(program_type: str) -> Path:
    """Get destination directory for a program type."""
    subdir = TYPE_DIRS.get(program_type, "Experts")
    return MQL5_DIR / subdir


def cmd_compile(args):
    """Compile an MQ5 file using MetaEditor via Wine."""
    src = Path(args.file).resolve()
    if not src.exists():
        print(f"Error: {src} not found")
        return 1

    # Find metaeditor
    candidates = [
        MT5_BASE / "metaeditor64.exe",
        MT5_BASE / "metaeditor.exe",
    ]
    # Also check common alternative locations
    for p in MT5_BASE.rglob("metaeditor*.exe"):
        candidates.append(p)

    editor = None
    for c in candidates:
        if c.exists():
            editor = c
            break

    if not editor:
        print("Error: metaeditor.exe not found in MT5 installation")
        print(f"Searched: {MT5_BASE}")
        print("Compilation must be done manually in MetaEditor IDE.")
        return 1

    # Deploy first, then compile
    program_type = detect_type(src)
    dest_dir = get_dest_dir(program_type)
    dest = dest_dir / src.name

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Deployed: {src.name} → {dest}")

    # Compile via Wine
    try:
        result = subprocess.run(
            ["wine", str(editor), "/compile", str(dest), "/include", str(MQL5_DIR / "Include")],
            capture_output=True, text=True, timeout=30,
        )
        print(f"Compile output:\n{result.stdout}")
        if result.returncode != 0:
            print(f"Compile errors:\n{result.stderr}")
            return result.returncode
    except FileNotFoundError:
        print("Error: wine not found. Install wine first.")
        return 1
    except subprocess.TimeoutExpired:
        print("Compile timed out (30s). Check MetaEditor for errors.")
        return 1

    return 0


def cmd_deploy(args):
    """Deploy an MQ5 file to the correct MQL5 directory."""
    src = Path(args.file).resolve()
    if not src.exists():
        print(f"Error: {src} not found")
        return 1

    program_type = detect_type(src)
    dest_dir = get_dest_dir(program_type)
    dest = dest_dir / src.name

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print(f"Deployed: {src.name} → {dest}")
    print(f"Type: {program_type}")
    print(f"Compile in MetaEditor to generate .ex5")
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

    # Check account info via Wine terminal info
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
    parser = argparse.ArgumentParser(description="MQL5 development helper")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show MT5 installation status")
    sub.add_parser("list", help="List all MQ5 source files")

    compile_p = sub.add_parser("compile", help="Compile an MQ5 file")
    compile_p.add_argument("file", help="Path to .mq5 file")

    deploy_p = sub.add_parser("deploy", help="Deploy MQ5 to MQL5 directory")
    deploy_p.add_argument("file", help="Path to .mq5 file")

    args = parser.parse_args()

    if args.command == "status":
        return cmd_status(args)
    elif args.command == "list":
        return cmd_list(args)
    elif args.command == "compile":
        return cmd_compile(args)
    elif args.command == "deploy":
        return cmd_deploy(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
