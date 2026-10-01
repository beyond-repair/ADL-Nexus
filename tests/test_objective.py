"""Objective spine contracts. No empty xfail.

reality and provenance are PATHWAY_SPEC entries for the actions that exist.
Unknown actions still deny. think/authorize/commit are kernel methods.
commit assigns a workforce task; it does not execute the role.
"""

from core.kernel import NexusKernel
from layer3_workforce.roles import list_tasks
from layer8_economic.provenance import list_entries


def test_think_does_not_execute():
    k = NexusKernel().bootstrap()
    thought = k.think("review layer0")
    assert thought["ok"] is True
    proposal = thought["proposal"]
    assert proposal["executed"] is False
    assert proposal["status"] == "proposed"
    assert proposal["authorized"] is False
    assert "advice" in thought["claim"]
    assert thought["reality"]["claim"].startswith("local reality snapshot")


def test_commit_refused_without_authorize():
    k = NexusKernel().bootstrap()
    thought = k.think("review layer0")
    committed = k.commit(thought["proposal"]["id"])
    assert committed["ok"] is False
    assert "unauthorized" in committed["error"]


def test_authorize_then_commit_assigns():
    k = NexusKernel().bootstrap()
    thought = k.think("review layer0")
    pid = thought["proposal"]["id"]
    auth = k.authorize(pid)
    assert auth["ok"] is True
    assert auth["proposal"]["authorized"] is True
    committed = k.commit(pid)
    assert committed["ok"] is True
    task = committed["proposal"]["assignment"]["task"]
    assert task["role"] == "engineer"
    assert task["status"] == "pending"
    assert committed["proposal"]["executed"] is True
    assert "no external deploy" in committed["claim"]
    pending = list_tasks("pending")
    assert any(t["id"] == task["id"] for t in pending["tasks"])
    prov = committed["provenance"]
    assert prov["ok"] is True
    assert prov["entry"]["kind"] == "commit"
    linked = [
        e for e in list_entries()["entries"]
        if e["payload"].get("proposal_id") == pid
    ]
    assert [e["kind"] for e in linked] == ["think", "authorize", "commit"]
    assert linked[1]["previous"] == linked[0]["id"]
    assert linked[2]["previous"] == linked[1]["id"]


def test_reality_and_provenance_pathways(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    import layer8_economic.provenance as prov

    prov._LOG = []
    prov._BOUND = None
    k = NexusKernel().bootstrap()
    reality = k.call("reality", "state", "review layer0")
    assert reality.ok is True and reality.allowed is True
    body = reality.result
    assert body["live"] is False
    assert body["live_realityos"] is False
    assert "RealityOS" in body["claim"]
    assert body["risk_cost_confidence"]["confidence_label"] == "hardcoded"
    assert all(row["confidence_label"] == "hardcoded" for row in body["simulated_outcomes"])
    info = k.call("reality", "info")
    assert info.ok and info.result["live"] is False
    assert info.result["live_realityos"] is False
    denied = k.call("reality", "deploy")
    assert denied.ok is False and denied.allowed is False
    assert "not declared" in denied.reason

    thought = k.think("review layer0")
    assert thought["ok"] is True
    listed = k.call("provenance", "list")
    assert listed.ok and listed.allowed is True
    entries = listed.result["entries"]
    assert entries
    assert entries[0]["previous"] == ""
    for prev, nxt in zip(entries, entries[1:]):
        assert nxt["previous"] == prev["id"]
    got = k.call("provenance", "get", entries[-1]["id"])
    assert got.ok and got.result["ok"] is True
    assert got.result["entry"]["id"] == entries[-1]["id"]
    unknown = k.call("provenance", "settle")
    assert unknown.ok is False and unknown.allowed is False
    assert "not declared" in unknown.reason
