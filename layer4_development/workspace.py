"""Layer 4 — Development workspace (claim-capped analysis surface)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from analysis.repo import analyze_tree


class DevWorkspace:
    """Repository analysis / future refactor surface. Not a codegen product."""

    name = "development"
    layer = 4
    claim_level = 2
    capabilities = ("analyze", "list_entrypoints", "info")

    def analyze(self, path: str | Path = ".") -> dict[str, Any]:
        result = analyze_tree(path)
        result["subsystem"] = self.name
        result["claim_level"] = self.claim_level
        return result

    def list_entrypoints(self, path: str | Path = ".") -> dict[str, Any]:
        root = Path(path)
        hits = []
        for name in ("run.py", "core/nexus.py", "core/__main__.py", "pyproject.toml"):
            p = root / name
            hits.append({"path": name, "exists": p.exists()})
        return {"ok": True, "entrypoints": hits, "claim_level": self.claim_level}

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "layer": self.layer,
            "claim_level": self.claim_level,
            "capabilities": list(self.capabilities),
            "status": "scaffolded-active",
        }
