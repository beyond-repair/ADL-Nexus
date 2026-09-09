from layer3_workforce.roles import (
    assign,
    complete,
    execute,
    get_role,
    list_roles,
    list_tasks,
    run_goal,
)
from layer3_workforce.store import load_tasks


def test_roles_exist():
    roles = list_roles()
    assert "engineer" in roles
    assert "researcher" in roles
    r = get_role("engineer")
    assert "code" in r.capabilities


def test_assign_survives_reload(tmp_path, monkeypatch):
    monkeypatch.setenv("NEXUS_STATE_DIR", str(tmp_path / ".nexus"))
    assigned = assign("engineer", "analyze repository")
    assert assigned["ok"]
    tid = assigned["task"]["id"]
    reloaded = load_tasks()
    assert tid in reloaded
    assert reloaded[tid]["goal"] == "analyze repository"


def test_complete_without_execute_refused(tmp_path, monkeypatch):
    monkeypatch.setenv("NEXUS_STATE_DIR", str(tmp_path / ".nexus"))
    assigned = assign("engineer", "analyze repository")
    tid = assigned["task"]["id"]
    denied = complete(tid)
    assert denied["ok"] is False
    assert "provenance" in denied["error"]


def test_positive_execute_path(tmp_path, monkeypatch):
    monkeypatch.setenv("NEXUS_STATE_DIR", str(tmp_path / ".nexus"))
    out = run_goal("analyze repository", {"path": "."})
    assert out["ok"]
    executed = out["executed"]
    assert executed["result"] == "SUCCESS"
    assert executed["adapter_output"]["adapter"] == "sunder"
    assert executed["provenance"]["result"] == "SUCCESS"
    assert executed["provenance"]["adapter"] == "sunder"
    from pathlib import Path
    assert Path(executed["provenance_path"]).exists()
    assert out["completed"]["task"]["status"] == "complete"
    pending = list_tasks("complete")
    assert pending["count"] >= 1


def test_refusal_path(tmp_path, monkeypatch):
    monkeypatch.setenv("NEXUS_STATE_DIR", str(tmp_path / ".nexus"))
    out = run_goal("forbidden claim: live RealityOS twin is production ready")
    assert out["ok"] is False
    executed = out["executed"]
    assert executed["result"] == "REFUSED"
    assert executed["task"]["status"] == "refused"
    denied = complete(executed["task"]["id"])
    assert denied["ok"] is False
    assert denied["provenance"]["result"] == "REFUSED"
