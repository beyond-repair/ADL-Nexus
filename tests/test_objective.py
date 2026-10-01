"""Objective spine contracts. No empty xfail.

reality and provenance stay off PATHWAY_SPEC. kernel.call fails closed
with unknown pathway. think/authorize/commit are kernel methods. commit
assigns a workforce task; it does not execute the role.
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
    kinds = {e["kind"] for e in list_entries()["entries"] if e["payload"].get("proposal_id") == pid}
    assert kinds == {"think", "authorize", "commit"}


def test_reality_and_provenance_pathways():
    k = NexusKernel().bootstrap()
    reality = k.call("reality", "state", "review layer0")
    assert reality.ok is False
    assert reality.allowed is False
    assert reality.reason == "unknown pathway: reality"
    provenance = k.call("provenance", "list")
    assert provenance.ok is False
    assert provenance.reason == "unknown pathway: provenance"
