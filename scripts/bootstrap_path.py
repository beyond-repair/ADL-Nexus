#!/usr/bin/env python3
"""Auto-detect sibling checkouts of sunder and sovereign-clean-room and prepend to sys.path.

Usage:
  python scripts/bootstrap_path.py          # print detected paths
  eval $(python scripts/bootstrap_path.py --export)  # shell export PYTHONPATH

Also importable:
  from scripts.bootstrap_path import ensure_paths
  ensure_paths()
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path

# ADL-Nexus root (parent of scripts/)
NEXUS_ROOT = Path(__file__).resolve().parents[1]

# Candidate locations relative to Nexus root and common monorepo layouts
CANDIDATES = [
    NEXUS_ROOT.parent / "sovereign-clean-room",
    NEXUS_ROOT.parent / "sunder",
    NEXUS_ROOT / "vendor" / "sovereign-clean-room",
    NEXUS_ROOT / "vendor" / "sunder",
    Path.home() / "src" / "sovereign-clean-room",
    Path.home() / "src" / "sunder",
    Path.home() / "code" / "sovereign-clean-room",
    Path.home() / "code" / "sunder",
]

MARKERS = {
    "sovereign-clean-room": ["core/clean_room_vsa.py", "core/clean_room_cli.py"],
    "sunder": ["sunder/__init__.py", "pyproject.toml"],
}


def _looks_like(repo_dir: Path, kind: str) -> bool:
    if not repo_dir.is_dir():
        return False
    for marker in MARKERS.get(kind, []):
        if (repo_dir / marker).exists():
            return True
    return False


def discover() -> dict[str, Path]:
    found: dict[str, Path] = {}
    for p in CANDIDATES:
        name = p.name
        if name in ("sovereign-clean-room", "sunder") and name not in found:
            if _looks_like(p, name):
                found[name] = p.resolve()
    return found


def ensure_paths(verbose: bool = False) -> dict[str, Path]:
    """Prepend discovered roots to sys.path. Returns dict of found repos."""
    found = discover()
    for name, path in found.items():
        sp = str(path)
        if sp not in sys.path:
            sys.path.insert(0, sp)
            if verbose:
                print(f"[bootstrap] added {name}: {sp}", file=sys.stderr)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="ADL Nexus path bootstrap")
    parser.add_argument("--export", action="store_true", help="Print export PYTHONPATH=... for eval")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    found = discover()
    if args.export:
        parts = [str(p) for p in found.values()]
        existing = __import__("os").environ.get("PYTHONPATH", "")
        if existing:
            parts.append(existing)
        print("export PYTHONPATH=" + ":".join(parts))
        return 0

    if not found:
        print("No sibling checkouts detected.")
        print("Searched:")
        for p in CANDIDATES:
            print(f"  {p}")
        return 1

    for name, path in found.items():
        print(f"{name}: {path}")
    if args.verbose:
        ensure_paths(verbose=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
