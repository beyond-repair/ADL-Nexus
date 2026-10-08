from core.kernel import NexusKernel
from layer3_workforce.roles import assign, list_tasks, complete
from layer5_security.integrity import save_anchor, check_anchor, ANCHOR_FILE
from pathlib import Path


def test_runtime_pathway_execute():
    k = NexusKernel().bootstrap()
    ran = k.call("runtime", "execute", "echo hello", {})
    assert ran.ok, ran.reason
    assert ran.allowed is True
    assert ran.result.success is True
    assert ran.result.steps == ["echo"]
    missing = k.call("runtime", "not_a_tool")
    assert missing.ok is False
    assert missing.allowed is False
    assert "not declared" in missing.reason


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
    out = k.request("analyze repository")
    assert out["ok"] is False
    assert out["fail_closed"] is True
    assert out["error"] == "unavailable: NexusKernel.request is not implemented"


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
    out = k.serve_loopback(host="127.0.0.1", port=9)
    assert out["ok"] is False
    assert out["fail_closed"] is True
    assert out["bound"] is False
    assert out["error"] == "unavailable: NexusKernel.serve_loopback is not implemented"


def test_nexus_run_is_governed(tmp_path, monkeypatch):
    import sys
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["nexus", "run", "--goal", "echo only", "--path", str(tmp_path)])
    from core.nexus import main
    from layer0_governance.registry import get_audit_log
    before = len(get_audit_log())
    assert main() == 0
    actions = [e.get("action") for e in get_audit_log()[before:] if e.get("event") == "evaluate"]
    assert "execute" in actions
    assert "echo" in actions
    assert "run_goal" in actions
    assert "put" in actions


def test_execute_checks_each_tool():
    k = NexusKernel().bootstrap()
    k.runtime.plan = lambda goal: ["exfiltrate"]
    k.runtime.register_tool("exfiltrate", lambda goal, context: "no")
    result = k.runtime.execute("nope", {})
    assert result.success is False
    assert result.message.startswith("governance:")
