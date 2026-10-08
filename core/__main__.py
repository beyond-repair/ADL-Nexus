"""python -m core [command]  (defaults to `status`, same as run.py)"""

import sys

from .nexus import main

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv.append("status")
    raise SystemExit(main())
