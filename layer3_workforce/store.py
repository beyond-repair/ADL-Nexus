"""Persistent task board. Process restart must not drop tasks (NEX-INT-001 I3)."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def state_dir() -> Path:
    raw = os.environ.get("NEXUS_STATE_DIR", ".nexus")
    path = Path(raw)
    path.mkdir(parents=True, exist_ok=True)
    (path / "provenance").mkdir(parents=True, exist_ok=True)
    return path


def tasks_path() -> Path:
    return state_dir() / "tasks.json"


def load_tasks() -> dict[str, dict[str, Any]]:
    p = tasks_path()
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    if isinstance(data, dict) and "tasks" in data and isinstance(data["tasks"], dict):
        return data["tasks"]
    if isinstance(data, dict):
        return {k: v for k, v in data.items() if isinstance(v, dict)}
    return {}


def save_tasks(tasks: dict[str, dict[str, Any]]) -> Path:
    p = tasks_path()
    payload = {"claim": "supervised board; not autonomy", "tasks": tasks}
    p.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n", encoding="utf-8")
    return p
