"""Claim-capped adapter toward sovereign-clean-room VSA memory.

Real surface (when available on PYTHONPATH):
  from core.clean_room_vsa import CleanRoomVSAEngine, CleanRoomGate

Target: FHRR / BaNEL / hyperspherical memory as single source of truth.
Fail-soft: stub local dict when import fails. Deep production interop still claim-capped.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional
import time

@dataclass
class CleanRoomStatus:
    available: bool
    mode: str  # "live" | "stub"
    message: str
    engine_dim: int | None = None

class CleanRoomAdapter:
    def __init__(self, dim: int = 1024):
        self._engine = None
        self._gate = None
        self._local: dict[str, Any] = {}
        self._dim_request = dim
        self.status = self._detect()

    def _detect(self) -> CleanRoomStatus:
        # Try several import styles that match the sovereign-clean-room layout
        candidates = [
            "core.clean_room_vsa",
            "clean_room_vsa",
        ]
        last_err = "not found"
        for mod_name in candidates:
            try:
                import importlib
                mod = importlib.import_module(mod_name)
                Engine = getattr(mod, "CleanRoomVSAEngine", None)
                Gate = getattr(mod, "CleanRoomGate", None)
                if Engine is None:
                    continue
                # Use a modest dim for adapter smoke tests unless upstream defaults differ
                self._engine = Engine(dim=self._dim_request)
                if Gate is not None:
                    self._gate = Gate(self._engine)
                # Jump-start protected atoms when possible
                if hasattr(self._engine, "jump_start_v01"):
                    try:
                        self._engine.jump_start_v01()
                    except Exception:
                        pass
                return CleanRoomStatus(
                    True, "live",
                    f"CleanRoomVSAEngine loaded from {mod_name}",
                    engine_dim=getattr(self._engine, "dim", None),
                )
            except Exception as e:
                last_err = f"{e.__class__.__name__}: {e}"
                continue
        return CleanRoomStatus(False, "stub", f"clean-room not available ({last_err})")

    # --- unified surface ---

    def put(self, key: str, value: Any) -> str:
        if self.status.available and self._engine is not None:
            # Register a named symbol; value is stored as metadata only in this adapter layer
            try:
                self._engine.register(key, meta={"payload_type": type(value).__name__, "ts": time.time()})
                self._local[key] = value  # keep python-side payload alongside
                return f"live:{key}"
            except Exception as e:
                self._local[key] = value
                return f"fallback:{key}:{e.__class__.__name__}"
        self._local[key] = value
        return f"stub:{key}"

    def get(self, key: str, default: Any = None) -> Any:
        return self._local.get(key, default)

    def query(self, probe_name: str, top_k: int = 5) -> list:
        if not (self.status.available and self._engine is not None):
            return []
        vec = self._engine.get(probe_name)
        if vec is None:
            return []
        try:
            return self._engine.query(vec, top_k=top_k)
        except Exception:
            return []

    def stats(self) -> dict[str, Any]:
        if self.status.available and self._engine is not None and hasattr(self._engine, "codebook_stats"):
            try:
                return self._engine.codebook_stats()
            except Exception as e:
                return {"error": str(e)}
        return {"mode": "stub", "local_keys": len(self._local)}

    def info(self) -> dict[str, Any]:
        return {
            "adapter": "cleanroom",
            "status": self.status.__dict__,
            "local_keys": list(self._local.keys()),
            "stats": self.stats(),
            "claim": "claim-capped; live engine used when importable, else stub",
        }
