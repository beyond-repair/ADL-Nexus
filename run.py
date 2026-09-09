#!/usr/bin/env python3
"""Zero-install runner for ADL Nexus.

Usage (from the repo root, no pip required):

    python run.py
    python run.py status
    python run.py packages
    python run.py layers
    python run.py call --pathway development --action analyze --kw path=.
    python run.py run --goal "analyze repository"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _nex_int_run(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="run.py run")
    parser.add_argument("--goal", default="analyze repository")
    parser.add_argument("--path", default=".")
    args, _ = parser.parse_known_args(argv)
    from layer3_workforce.roles import run_goal
    loop = run_goal(args.goal, {"path": args.path}, role="engineer")
    executed = loop.get("executed") or {}
    print("Task Assigned:", (loop.get("assigned") or {}).get("ok"))
    print("Reality Check:", (executed.get("gate") or {}).get("reason"))
    print("Adapter Executed:", executed.get("result"), (executed.get("adapter_output") or {}).get("adapter"))
    print("Provenance Written:", executed.get("provenance_path"), (executed.get("provenance") or {}).get("result"))
    print("Task Completed:", (loop.get("completed") or {}).get("ok"))
    if executed.get("result") == "REFUSED":
        return 2
    return 0 if loop.get("ok") else 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("status")
    if len(sys.argv) >= 2 and sys.argv[1] == "run":
        raise SystemExit(_nex_int_run(sys.argv[2:]))
    from core.nexus import main
    raise SystemExit(main())
