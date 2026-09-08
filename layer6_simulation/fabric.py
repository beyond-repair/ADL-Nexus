"""Layer 6 — Simulation fabric (registration only; no live world claim)."""

from __future__ import annotations

from typing import Any


class SimulationFabric:
    name = "simulation"
    layer = 6
    claim_level = 2
    capabilities = ("register", "list", "info")

    def __init__(self) -> None:
        self._worlds: dict[str, dict[str, Any]] = {
            "nexus-party": {
                "kind": "godot-client",
                "path": "client/godot_nexus_party",
                "live": False,
                "note": "client scaffold; not a running sim kernel",
            },
            "pixel-chat": {
                "kind": "web-client",
                "path": "client/web_pixel_chat",
                "live": False,
            },
        }

    def register(self, world_id: str, kind: str = "unspecified", **meta: Any) -> dict[str, Any]:
        entry = {"kind": kind, "live": False, **meta}
        self._worlds[world_id] = entry
        return {"ok": True, "world_id": world_id, "entry": entry, "claim_level": self.claim_level}

    def list(self) -> dict[str, Any]:
        return {"ok": True, "worlds": dict(self._worlds), "claim_level": self.claim_level}

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "layer": self.layer,
            "claim_level": self.claim_level,
            "capabilities": list(self.capabilities),
            "world_count": len(self._worlds),
            "status": "scaffolded-active",
        }
