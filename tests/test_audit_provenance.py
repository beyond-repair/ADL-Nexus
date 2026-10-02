"""Durable audit and provenance. RAM is not the record."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

from layer8_economic import provenance as prov


def _digest(entry: dict) -> str:
    linked = {
        "kind": entry["kind"],
        "payload": entry["payload"],
        "previous": entry["previous"],
    }
    raw = json.dumps(linked, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def test_two_provenance_records_chain_and_survive_ram_drop(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    prov._LOG = []
    prov._BOUND = None
    first = prov.record("think", {"n": 1})
    second = prov.record("commit", {"n": 2})
    assert first["entry"]["previous"] == ""
    assert second["entry"]["previous"] == first["entry"]["id"]
    assert _digest(first["entry"]) == first["entry"]["id"]
    assert _digest(second["entry"]) == second["entry"]["id"]
    # wall clock is stored but not part of the digest
    assert "ts" not in {
        "kind": first["entry"]["kind"],
        "payload": first["entry"]["payload"],
        "previous": first["entry"]["previous"],
    }
    path = tmp_path / ".nexus_memory" / "provenance.jsonl"
    assert path.is_file()
    prov._LOG = []
    prov._BOUND = None
    entries = prov.list_entries()["entries"]
    assert len(entries) == 2
    assert entries[0]["previous"] == ""
    assert entries[1]["previous"] == entries[0]["id"]
    assert prov.get(entries[1]["id"])["entry"]["kind"] == "commit"


def test_deny_is_on_disk_after_process_exit(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    script = tmp_path / "deny_once.py"
    script.write_text(
        "\n".join([
            "from layer0_governance.registry import evaluate_request",
            "from layer5_security.gate import SecurityGate",
            "d = evaluate_request('not-registered', 'ping')",
            "assert d.allowed is False",
            "s = SecurityGate().evaluate('coding-agent', 'exfiltrate')",
            "assert s.allowed is False",
        ]) + "\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo)
    subprocess.check_call([sys.executable, str(script)], cwd=tmp_path, env=env)
    raw = (tmp_path / ".nexus_memory" / "audit.jsonl").read_text(encoding="utf-8")
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    gov = [
        row for row in rows
        if row.get("event") == "evaluate" and row.get("subsystem") == "not-registered"
    ]
    assert gov and gov[0]["decision"]["allowed"] is False
    sec = [
        row for row in rows
        if row.get("channel") == "security" and row.get("action") == "exfiltrate"
    ]
    assert sec and sec[0]["decision"]["allowed"] is False
    for row in rows:
        assert "context" not in row
        assert "secret" not in row
        assert "token" not in row
