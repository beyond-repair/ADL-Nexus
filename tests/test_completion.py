import pytest
from core.kernel import NexusKernel
from layer3_workforce.roles import assign, list_tasks, complete
from layer5_security.integrity import save_anchor, check_anchor, ANCHOR_FILE
from pathlib import Path


def test_runtime_pathway_execute():
    """Spine incomplete: runtime pathway has no 'execute' action under current PATHWAY_SPEC."""
    pytest.xfail("RESEARCH claim-cap: runtime execute not declared; see Sweep-131")


def test_workforce_supervised_assign():
    assigned = assign("engineer", "review layer0")
    assert assigned["ok"]
    tid = assigned["task"]["id"]
    pending = list_tasks("pending")
    assert any(t["id"] == tid for t in pending["tasks"])
    done = complete(tid, "reviewed")
    assert done["ok"]
    assert done["task"]["status"] == "complete"


def test_kernel_request_loop():
    pytest.xfail("RESEARCH claim-cap: NexusKernel.request not implemented; Sweep-131")


def test_optional_integrity_anchor(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sample = Path("sample.txt")
    sample.write_text("anchor-me", encoding="utf-8")
    saved = save_anchor(sample, label="t1")
    assert saved["ok"]
    assert ANCHOR_FILE.exists()
    checked = check_anchor("t1")
    assert checked["ok"]


def test_loopback_host_refused():
    pytest.xfail("RESEARCH claim-cap: NexusKernel.serve_loopback not implemented; Sweep-131")
