"""Layer 8 — Economic ledger stub (no billing, no marketplace claim)."""

from __future__ import annotations

from typing import Any


class EconomicLedger:
    name = "economic"
    layer = 8
    claim_level = 1
    capabilities = ("record", "balance", "info")

    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    def record(self, kind: str, amount: float = 0.0, note: str = "") -> dict[str, Any]:
        entry = {"kind": kind, "amount": float(amount), "note": note, "settled": False}
        self._entries.append(entry)
        return {"ok": True, "entry": entry, "claim_level": self.claim_level}

    def balance(self) -> dict[str, Any]:
        total = sum(e["amount"] for e in self._entries)
        return {
            "ok": True,
            "entries": len(self._entries),
            "nominal_sum": total,
            "settled": False,
            "claim_level": self.claim_level,
            "note": "nominal only — not a payment system",
        }

    def info(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "layer": self.layer,
            "claim_level": self.claim_level,
            "capabilities": list(self.capabilities),
            "status": "scaffolded",
        }
