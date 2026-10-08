"""Minimal artifact integrity helpers (forge-aegis inspired).

Same inputs → same hash. Fail-closed on read errors: tree_hash raises
OSError for an unreadable file and does not hash the placeholder
b"<unreadable>". Not a full AEGIS pipeline; claim-capped local
verification only.

Anchors are stored in `.nexus_anchors.json` in the current working
directory (ANCHOR_FILE). There is no `.nexus/anchors.json` writer.
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
            payload = p.read_bytes()
        except OSError as exc:
            raise OSError(f"unreadable file: {rel}") from exc
        h.update(payload)
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


# --- Anchor helpers (claim-capped local only) ---
# Simple file-backed labels for optional integrity checks in tests / local use.
# Not a full forge-aegis pipeline.

import json
from datetime import datetime, timezone

# Single anchor filename. ROADMAP and CLAIM_STATUS use this same path.
ANCHOR_FILE = Path(".nexus_anchors.json")


def save_anchor(path: str | Path, label: str, algo: str = "sha256") -> dict:
    """Persist a labeled hash of path under `.nexus_anchors.json` (cwd).

    Idempotent overwrite of label. Read errors from tree_hash propagate
    (fail closed); they are not stored as a successful anchor.
    """
    path = Path(path)
    if not path.exists():
        return {"ok": False, "error": "path not found", "path": str(path)}
    if path.is_file():
        digest = file_hash(path, algo=algo)
        kind = "file"
    elif path.is_dir():
        digest = tree_hash(path, algo=algo)
        kind = "dir"
    else:
        return {"ok": False, "error": "unsupported path type", "path": str(path)}

    data: dict = {}
    if ANCHOR_FILE.exists():
        try:
            data = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            data = {}

    data[label] = {
        "path": str(path.resolve()) if path.is_absolute() else str(path),
        "kind": kind,
        "algo": algo,
        "hash": digest,
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "claim": "local integrity check only; not full forge-aegis pipeline",
    }
    try:
        ANCHOR_FILE.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    except OSError as e:
        return {"ok": False, "error": str(e)}
    return {"ok": True, "label": label, "hash": digest, "path": str(path)}


def check_anchor(label: str, algo: str | None = None) -> dict:
    """Recompute hash for a saved label and compare. Fail-closed."""
    if not ANCHOR_FILE.exists():
        return {"ok": False, "error": "no anchor file"}
    try:
        data = json.loads(ANCHOR_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return {"ok": False, "error": f"unreadable anchors: {e}"}
    entry = data.get(label)
    if entry is None:
        return {"ok": False, "error": f"unknown label: {label}"}
    path = Path(entry["path"])
    use_algo = algo or entry.get("algo", "sha256")
    expected = entry.get("hash", "")
    return verify_anchor(path, expected, algo=use_algo)
