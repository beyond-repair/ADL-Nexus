"""Load vendored ADL-Governance text.

The files under imported/adl_governance are verbatim copies named in SOURCE.txt.
Loading them does not start a kernel, RealityOS, Sunder, or a clean-room engine.
The local registry remains the decision stand-in. This module only checks that
the pinned text is present and unchanged.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1] / "imported" / "adl_governance"
_REQUIRED_MARKERS = {
    "CONSTITUTION.md": (
        "Article 2 — Classification",
        "Article 4 — Claim integrity",
        "Cryptographic or CI success does **not** imply experimental physics validation.",
    ),
    "CLAIM_VALIDATION.md": (
        "| 0 | Idea |",
        "| 5 | Engineering validation |",
        "A green CI, ledger signature, or Merkle proof does **not** raise physics claim level.",
    ),
    "LIFECYCLE.md": (
        "Reference to ADL-Governance",
        "SECURITY.md present",
    ),
}


def _parse_source(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    hashes: dict[str, str] = {}
    for line in text.splitlines():
        if line.startswith("sha256 "):
            _tag, name, digest = line.split()
            hashes[name] = digest
            continue
        if ": " in line:
            key, value = line.split(": ", 1)
            fields[key] = value
    fields["hashes"] = hashes  # type: ignore[assignment]
    return fields


def load_import() -> dict[str, object]:
    """Fail closed when the pinned constitution text is missing or altered."""
    source_path = _ROOT / "SOURCE.txt"
    if not source_path.is_file():
        raise RuntimeError("ADL-Governance import missing SOURCE.txt")
    parsed = _parse_source(source_path.read_text(encoding="utf-8"))
    hashes: dict[str, str] = parsed["hashes"]  # type: ignore[assignment]
    if set(hashes) != set(_REQUIRED_MARKERS):
        raise RuntimeError("ADL-Governance SOURCE.txt file list does not match the required set")
    loaded: list[str] = []
    for name, markers in _REQUIRED_MARKERS.items():
        path = _ROOT / name
        if not path.is_file():
            raise RuntimeError(f"ADL-Governance import missing {name}")
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != hashes[name]:
            raise RuntimeError(f"ADL-Governance import hash mismatch for {name}")
        text = raw.decode("utf-8")
        for marker in markers:
            if marker not in text:
                raise RuntimeError(f"ADL-Governance import {name} missing required text")
        loaded.append(name)
    commit = parsed.get("commit")
    if not isinstance(commit, str) or len(commit) != 40:
        raise RuntimeError("ADL-Governance import commit is not a 40-character id")
    if parsed.get("published_claim_max") != "1":
        raise RuntimeError("published claim max must stay 1; no Level 2 evidence is recorded")
    if parsed.get("local_ceiling") != "2":
        raise RuntimeError("local ceiling must stay 2")
    return {
        "state": "docs-imported",
        "repository": parsed.get("repository"),
        "ref": parsed.get("ref"),
        "source_commit": commit,
        "files": sorted(loaded),
        "published_claim_max": 1,
        "local_ceiling": 2,
        "live_kernel": False,
        "realityos": False,
        "sunder_engine": False,
        "clean_room_engine": False,
    }
