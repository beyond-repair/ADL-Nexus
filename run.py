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

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.nexus import main


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("status")
    raise SystemExit(main())
