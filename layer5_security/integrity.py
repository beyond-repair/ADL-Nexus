"""Minimal artifact integrity helpers (forge-aegis inspired).

Same inputs → same hash. Fail-closed on read errors.
Not a full AEGIS pipeline; claim-capped local verification only.
"""

from __future__ import annotations
from pathlib import Path
from typing import Iterable
import hashlib


def file_hash(path: str | Path, algo: str = "sha256") -> str:
    path = Path(path)
    h = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_hash(root: str | Path, patterns: Iterable[str] | None = None, algo: str = "sha256") -> str:
    """Deterministic hash of file contents under root (sorted paths).

    patterns: optional suffix filters (e.g. [".py", ".md"]). None = all regular files.
    """
    root = Path(root)
    h = hashlib.new(algo)
    files = sorted(
        p for p in root.rglob("*")
        if p.is_file() and not any(part.startswith(".") for part in p.parts)
        and (patterns is None or p.suffix in patterns)
    )
    for p in files:
        rel = p.relative_to(root).as_posix()
        h.update(rel.encode())
        h.update(b"\0")
        try:
            h.update(p.read_bytes())
        except OSError:
            h.update(b"<unreadable>")
        h.update(b"\0")
    return h.hexdigest()


def verify_anchor(path: str | Path, expected: str, algo: str = "sha256") -> dict:
    """Compare current hash to an expected anchor."""
    path = Path(path)
    if path.is_file():
        current = file_hash(path, algo=algo)
    elif path.is_dir():
        current = tree_hash(path, algo=algo)
    else:
        return {"ok": False, "error": "path not found", "path": str(path)}
    ok = current.lower() == expected.lower()
    return {
        "ok": ok,
        "path": str(path),
        "algo": algo,
        "current": current,
        "expected": expected,
        "claim": "local integrity check only; not full forge-aegis pipeline",
    }
