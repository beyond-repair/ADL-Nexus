"""Sibling path bootstrap must not shadow this repo."""

import sys

from scripts import bootstrap_path as bp


def test_pyproject_sibling_does_not_take_sys_path_front(tmp_path, monkeypatch):
    sibling = tmp_path / "sunder"
    sibling.mkdir()
    (sibling / "pyproject.toml").write_text("[project]\nname = \"other\"\n", encoding="utf-8")
    core_pkg = sibling / "core"
    core_pkg.mkdir()
    (core_pkg / "__init__.py").write_text("SHADOWS = True\n", encoding="utf-8")
    monkeypatch.setattr(bp, "CANDIDATES", [sibling])
    front = sys.path[0]
    found = bp.ensure_paths()
    assert found == {}
    assert str(sibling.resolve()) not in sys.path
    assert sys.path[0] == front

    package = sibling / "sunder"
    package.mkdir()
    (package / "__init__.py").write_text("# sunder package\n", encoding="utf-8")
    found = bp.ensure_paths()
    resolved = str(sibling.resolve())
    try:
        assert found.get("sunder") == sibling.resolve()
        assert resolved in sys.path
        assert sys.path[0] != resolved
        assert sys.path[0] == front
    finally:
        sys.path = [entry for entry in sys.path if entry != resolved]
