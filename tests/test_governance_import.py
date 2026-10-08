"""The vendored constitution is text, not a live engine."""

from pathlib import Path

import pytest

from layer0_governance.imported_constitution import load_import


def test_import_is_pinned_text_not_a_live_engine():
    report = load_import()
    assert report["state"] == "docs-imported"
    assert report["source_commit"] == "c2f677ff9613fc2c9614535b1bb34e1b3d8857ed"
    assert report["files"] == ["CLAIM_VALIDATION.md", "CONSTITUTION.md", "LIFECYCLE.md"]
    assert report["published_claim_max"] == 1
    assert report["local_ceiling"] == 2
    assert report["live_kernel"] is False
    assert report["realityos"] is False
    assert report["sunder_engine"] is False
    assert report["clean_room_engine"] is False


def test_kernel_status_reports_the_same_import():
    from core.kernel import NexusKernel

    status = NexusKernel().status()
    assert status["lifecycle"] == "RESEARCH"
    assert status["claim_cap"] == 2
    assert status["adl_governance"]["state"] == "docs-imported"
    assert status["adl_governance"]["live_kernel"] is False


def test_altered_constitution_fails_closed(tmp_path, monkeypatch):
    import layer0_governance.imported_constitution as mod

    source = Path(mod.__file__).resolve().parents[1] / "imported" / "adl_governance"
    broken = tmp_path / "adl_governance"
    broken.mkdir()
    for path in source.iterdir():
        (broken / path.name).write_bytes(path.read_bytes())
    constitution = broken / "CONSTITUTION.md"
    constitution.write_text(constitution.read_text(encoding="utf-8") + "\nrewritten\n", encoding="utf-8")
    monkeypatch.setattr(mod, "_ROOT", broken)
    with pytest.raises(RuntimeError, match="hash mismatch"):
        load_import()
