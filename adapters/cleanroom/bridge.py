"""Claim-capped adapter toward sovereign-clean-room VSA memory.

The upstream import `core.clean_room_vsa` collides with this repository's
`core` package, so discovery does not import that name. A sibling checkout
is loaded from its file path under a private module name. If that file is
missing, status mode is "unavailable" (not a crash, not a live engine).

get() never returns the local dict as if it were the external engine.
A local put is labeled source "local-stub". Fail-soft: Core still imports.
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import importlib
import importlib.util

@dataclass
class CleanRoomStatus:
    available: bool
    mode: str  # "live" | "unavailable"
    message: str
    engine_dim: int | None = None

class CleanRoomAdapter:
    def __init__(self, dim: int = 1024):
        self._engine = None
        self._gate = None
        self._local: dict[str, Any] = {}
        self._dim_request = dim
        self.status = self._detect()

    def _candidate_files(self) -> tuple[list[Path], str]:
        try:
            from scripts.bootstrap_path import CANDIDATES, discover
        except ImportError as e:
            return [], f"bootstrap_path unavailable ({type(e).__name__}: {e})"
        found = discover()
        roots: list[Path] = []
        hit = found.get("sovereign-clean-room")
        if hit is not None:
            roots.append(Path(hit))
        for candidate in CANDIDATES:
            if candidate.name == "sovereign-clean-room":
                roots.append(Path(candidate))
        files: list[Path] = []
        seen: set[Path] = set()
        for root in roots:
            path = root / "core" / "clean_room_vsa.py"
            if path.is_file():
                resolved = path.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    files.append(resolved)
        if not files:
            return [], (
                "clean-room engine unavailable (no sovereign-clean-room "
                "core/clean_room_vsa.py; import core.clean_room_vsa is not used "
                "because it collides with this repo's core package)"
            )
        return files, ""

    def _load_file(self, path: Path):
        spec = importlib.util.spec_from_file_location(
            "nexus_external_clean_room_vsa", path
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"cannot load clean-room engine from {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def _detect(self) -> CleanRoomStatus:
        files, missing = self._candidate_files()
        errors: list[str] = []
        module = None
        loaded_from = ""
        for path in files:
            try:
                module = self._load_file(path)
                loaded_from = str(path)
                break
            except Exception as e:
                # External file failed to load. Record it and keep looking.
                # Do not report live. The message stays on the status object.
                errors.append(f"{path.name}: {type(e).__name__}: {e}")
                module = None
        if module is None:
            try:
                module = importlib.import_module("clean_room_vsa")
                loaded_from = "clean_room_vsa"
            except ImportError as e:
                detail = missing or "clean-room engine unavailable"
                if errors:
                    detail = detail + "; " + "; ".join(errors)
                if not missing:
                    detail = f"{detail}; top-level clean_room_vsa: {type(e).__name__}: {e}"
                return CleanRoomStatus(False, "unavailable", detail)
            except Exception as e:
                return CleanRoomStatus(
                    False, "unavailable",
                    f"clean-room engine unavailable ({type(e).__name__}: {e})",
                )
        engine_cls = getattr(module, "CleanRoomVSAEngine", None)
        if engine_cls is None:
            return CleanRoomStatus(
                False, "unavailable",
                f"clean-room engine unavailable ({loaded_from} has no CleanRoomVSAEngine)",
            )
        try:
            self._engine = engine_cls(dim=self._dim_request)
        except Exception as e:
            self._engine = None
            return CleanRoomStatus(
                False, "unavailable",
                f"clean-room engine unavailable (construct failed {type(e).__name__}: {e})",
            )
        gate_cls = getattr(module, "CleanRoomGate", None)
        if gate_cls is not None:
            try:
                self._gate = gate_cls(self._engine)
            except Exception as e:
                self._gate = None
                return CleanRoomStatus(
                    True, "live",
                    f"CleanRoomVSAEngine loaded from {loaded_from}; gate not constructed ({type(e).__name__}: {e})",
                    engine_dim=getattr(self._engine, "dim", None),
                )
        return CleanRoomStatus(
            True, "live",
            f"CleanRoomVSAEngine loaded from {loaded_from}",
            engine_dim=getattr(self._engine, "dim", None),
        )

    def put(self, key: str, value: Any) -> dict[str, Any]:
        """Store a payload. Local dict writes are never labeled as engine results."""
        if self.status.mode != "live" or self._engine is None:
            self._local[key] = value
            return {"ok": True, "ref": f"stub:{key}", "source": "local-stub", "engine": False}
        for meth in ("put", "store", "upsert"):
            fn = getattr(self._engine, meth, None)
            if not callable(fn):
                continue
            try:
                fn(key, value)
            except TypeError:
                continue
            except Exception as e:
                return {
                    "ok": False,
                    "source": "engine",
                    "engine": True,
                    "error": f"{type(e).__name__}: {e}",
                }
            return {"ok": True, "ref": f"live:{key}", "source": "engine", "engine": True}
        return {
            "ok": False,
            "source": "engine",
            "engine": False,
            "error": "unavailable: engine has no payload put; local dict was not used as the result",
        }

    def get(self, key: str, default: Any = None) -> dict[str, Any]:
        """Read a value. source is 'engine' only when the external engine answers."""
        if self.status.mode == "live" and self._engine is not None:
            fn = getattr(self._engine, "get", None)
            if not callable(fn):
                return {
                    "ok": False,
                    "source": "engine",
                    "engine": True,
                    "value": None,
                    "error": "engine has no get",
                }
            try:
                value = fn(key)
            except Exception as e:
                return {
                    "ok": False,
                    "source": "engine",
                    "engine": True,
                    "value": None,
                    "error": f"{type(e).__name__}: {e}",
                }
            if value is None:
                value = default
            return {"ok": True, "source": "engine", "engine": True, "value": value}
        if key in self._local:
            return {"ok": True, "source": "local-stub", "engine": False, "value": self._local[key]}
        return {
            "ok": False,
            "source": "local-stub",
            "engine": False,
            "value": default,
            "error": "unavailable: clean-room engine not loaded",
        }

    def query(self, probe_name: str, top_k: int = 5) -> dict[str, Any]:
        """Not a PATHWAY_SPEC action. SecurityGate denies action 'query' at trust 0.25."""
        if self.status.mode != "live" or self._engine is None:
            return {
                "ok": False,
                "source": "local-stub",
                "error": "unavailable: clean-room engine not loaded",
                "hits": [],
            }
        get_fn = getattr(self._engine, "get", None)
        query_fn = getattr(self._engine, "query", None)
        if not callable(get_fn) or not callable(query_fn):
            return {
                "ok": False,
                "source": "engine",
                "error": "unavailable: engine has no query",
                "hits": [],
            }
        try:
            vec = get_fn(probe_name)
            if vec is None:
                return {"ok": True, "source": "engine", "hits": []}
            hits = query_fn(vec, top_k=top_k)
        except Exception as e:
            return {"ok": False, "source": "engine", "error": f"{type(e).__name__}: {e}", "hits": []}
        return {"ok": True, "source": "engine", "hits": hits}

    def stats(self) -> dict[str, Any]:
        if self.status.mode == "live" and self._engine is not None and hasattr(self._engine, "codebook_stats"):
            try:
                stats = self._engine.codebook_stats()
            except Exception as e:
                return {"ok": False, "source": "engine", "error": f"{type(e).__name__}: {e}"}
            if isinstance(stats, dict):
                stats = dict(stats)
                stats.setdefault("source", "engine")
                return stats
            return {"ok": True, "source": "engine", "stats": stats}
        return {"mode": "unavailable", "source": "local-stub", "local_keys": len(self._local)}

    def info(self) -> dict[str, Any]:
        live = self.status.mode == "live"
        return {
            "adapter": "cleanroom",
            "status": self.status.__dict__,
            "local_keys": list(self._local.keys()),
            "stats": self.stats(),
            "claim": (
                "external engine loaded; get() reads the engine, not the local dict"
                if live else
                "clean-room engine unavailable; local dict is a stub, not the external engine"
            ),
        }
