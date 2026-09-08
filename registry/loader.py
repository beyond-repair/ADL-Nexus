"""Minimal YAML-subset loader for the local registry manifests.

Stdlib only. Understands the shallow key/list style used in this repo.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def _parse_simple(text: str) -> dict[str, Any]:
    """Parse a tiny YAML subset: scalars, lists of scalars, one-level maps."""
    data: dict[str, Any] = {}
    pending_list: list[Any] | None = None
    current_map_list: list[dict[str, Any]] | None = None
    current_item: dict[str, Any] | None = None
    current_item_indent = 0

    def _coerce(v: str) -> Any:
        v = v.strip().strip('"').strip("'")
        if v.lower() in ("true", "yes"):
            return True
        if v.lower() in ("false", "no"):
            return False
        if v.isdigit():
            return int(v)
        return v

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        i += 1
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if line.startswith("- "):
            rest = line[2:]
            if current_map_list is not None and ":" in rest:
                current_item = {}
                current_map_list.append(current_item)
                k, _, v = rest.partition(":")
                current_item[k.strip()] = _coerce(v) if v.strip() else None
                current_item_indent = indent
            elif pending_list is not None:
                pending_list.append(_coerce(rest))
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if current_item is not None and indent > current_item_indent:
                current_item[k] = _coerce(v) if v else None
                continue
            if not v:
                nxt = None
                for peek in lines[i:]:
                    if peek.strip() and not peek.lstrip().startswith("#"):
                        nxt = peek
                        break
                if nxt and nxt.lstrip().startswith("- "):
                    lst: list[Any] = []
                    data[k] = lst
                    pending_list = lst
                    current_map_list = lst
                    current_item = None
                else:
                    nested: dict[str, Any] = {}
                    data[k] = nested
                    current_item = nested
                    current_item_indent = indent
                    pending_list = None
                    current_map_list = None
            else:
                data[k] = _coerce(v)
                pending_list = None
                current_map_list = None
                current_item = None
    return data


def load_manifests() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for p in sorted(ROOT.glob("*.yaml")):
        out[p.stem] = _parse_simple(p.read_text(encoding="utf-8"))
    return out


def list_manifests() -> list[str]:
    return sorted(p.stem for p in ROOT.glob("*.yaml"))
