from core.kernel import NexusKernel


def test_think_does_not_execute():
    k = NexusKernel().bootstrap()
    rec = k.think("analyze repository", {"path": "."})
    assert rec["ok"]
    proposal = rec["proposal"]
    assert proposal["authorized"] is False
    assert proposal["executed"] is False
    assert rec["reality"]["constraints"]["execute_requires_authorize"] is True


def test_commit_refused_without_authorize():
    k = NexusKernel().bootstrap()
    rec = k.think("research hypothesis")
    pid = rec["proposal"]["id"]
    denied = k.commit(pid)
    assert denied["ok"] is False
    assert "unauthorized" in denied["error"]


def test_authorize_then_commit_assigns():
    k = NexusKernel().bootstrap()
    rec = k.think("build a prototype")
    pid = rec["proposal"]["id"]
    auth = k.authorize(pid)
    assert auth["ok"]
    committed = k.commit(pid)
    assert committed["ok"]
    assert committed["proposal"]["executed"] is True
    assert committed["proposal"]["assignment"]["ok"]


def test_reality_and_provenance_pathways():
    k = NexusKernel().bootstrap()
    r = k.call("reality", "state", "what happens if we ship")
    assert r.ok, r.reason
    p = k.call("provenance", "list")
    assert p.ok, p.reason
