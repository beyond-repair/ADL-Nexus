"""Reality / claim gate. Forbidden inputs never reach sunder (NEX-INT-001 I4)."""

from __future__ import annotations

from typing import Any

FORBIDDEN_PHRASES = (
    "forbidden claim",
    "production ready",
    "production-ready",
    "full autonomous workforce",
    "full autonomy",
    "live realityos",
    "live digital double",
    "live sunder interop",
    "coherence drive product",
    "deploy payments",
    "move money",
)


def evaluate_claim(goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
    text = (goal or "").strip().lower()
    context = context or {}
    hits = [p for p in FORBIDDEN_PHRASES if p in text]
    if hits:
        return {
            "allowed": False,
            "result": "REFUSED",
            "reason": f"forbidden claim: {hits[0]}",
            "hits": hits,
            "goal": goal,
        }
    return {
        "allowed": True,
        "result": "PASS",
        "reason": "claim gate passed",
        "hits": [],
        "goal": goal,
        "context_keys": sorted(context),
    }
