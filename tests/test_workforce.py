from layer3_workforce.roles import (
    assign,
    complete,
    get_role,
    get_task,
    list_roles,
    list_tasks,
)
from layer3_workforce import roles as roles_mod


def test_roles_exist():
    roles = list_roles()
    assert "engineer" in roles
    assert "researcher" in roles
    r = get_role("engineer")
    assert "code" in r.capabilities


def _ids():
    return {task["id"] for task in list_tasks()["tasks"]}


def test_assign_rejects_unknown_role():
    before = _ids()
    out = assign("not-a-role", "do work", capability="code")
    assert out == {"ok": False, "error": "unknown role: not-a-role"}
    assert "task" not in out
    assert _ids() == before


def test_assign_rejects_capability_outside_contract():
    before = _ids()
    out = assign("engineer", "ship it", capability="deploy")
    assert out == {
        "ok": False,
        "error": "capability 'deploy' is not in engineer contract",
    }
    assert "task" not in out
    assert _ids() == before


def test_complete_rejects_missing_and_non_pending_task():
    missing = complete("does-not-exist")
    assert missing == {"ok": False, "error": "unknown task: does-not-exist"}
    assigned = assign("engineer", "review layer0", capability="code")
    assert assigned["ok"] is True
    tid = assigned["task"]["id"]
    roles_mod._BOARD[tid].status = "assigned"
    done = complete(tid, "reviewed")
    assert done["ok"] is True
    assert done["task"]["status"] == "complete"
    assert "output" not in done["task"]
    again = complete(tid, "actually did the work")
    assert again == {
        "ok": False,
        "error": f"task {tid} is complete; complete only accepts pending or assigned",
    }
    stored = get_task(tid)["task"]
    assert stored["status"] == "complete"
    assert stored["note"] == "reviewed"


def test_list_tasks_and_get_return_role_and_capability():
    assigned = assign("researcher", "check evidence", capability="evidence")
    assert assigned["ok"] is True
    tid = assigned["task"]["id"]
    listed = next(task for task in list_tasks()["tasks"] if task["id"] == tid)
    assert listed["role"] == "researcher"
    assert listed["capability"] == "evidence"
    got = get_task(tid)
    assert got["ok"] is True
    assert got["task"]["role"] == "researcher"
    assert got["task"]["capability"] == "evidence"
    assert got["task"]["status"] == "pending"
