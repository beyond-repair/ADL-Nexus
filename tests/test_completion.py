from core.kernel import NexusKernel
from layer3_workforce.roles import assign, list_tasks, complete
from layer5_security.integrity import save_anchor, check_anchor, ANCHOR_FILE
from pathlib import Path


def test_runtime_pathway_execute():
    k = NexusKernel().bootstrap()
    r = k.call("runtime", "execute", "analyze repository", {"path": "."})
    assert r.ok, r.reason
    assert r.result.success


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
    k = NexusKernel().bootstrap()
    rec = k.request("analyze repository", ".")
    assert rec["governance"]["allowed"]
    assert rec["runtime_ok"]
    assert rec["runtime"]["success"] is True
    assert k.memory.get("last_request") is not None


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
    k = NexusKernel().bootstrap()
    out = k.serve_loopback(host="0.0.0.0", port=1)
    assert out["ok"] is False
    assert "loopback" in out["error"]
