"""Stdlib-only tree analysis (no third-party deps)."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git", ".venv", "venv", "__pycache__", "node_modules",
    ".pytest_cache", "dist", "build", ".godot",
}


def analyze_tree(path: str | Path, limit: int = 200) -> dict[str, Any]:
    root = Path(path).resolve()
    if not root.exists():
        return {"ok": False, "error": f"missing path: {root}"}
    files: list[str] = []
    ext = Counter()
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file():
            rel = str(p.relative_to(root))
            files.append(rel)
            ext[p.suffix or "[none]"] += 1
            if len(files) >= limit:
                break
    return {
        "ok": True,
        "root": str(root),
        "file_count_sampled": len(files),
        "by_extension": dict(ext),
        "sample": files[:20],
        "claim_level": 2,
    }
