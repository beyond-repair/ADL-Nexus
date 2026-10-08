from core.pathways import list_pathways, probe_packages, describe
from core.kernel import NexusKernel


def test_all_packages_import():
    rows = probe_packages()
    failed = [r for r in rows if not r["import_ok"]]
    assert not failed, failed


def test_pathways_cover_layers():
    names = set(list_pathways())
    for required in (
        "governance", "memory", "runtime", "workforce", "development",
        "security", "simulation", "research", "economic", "sunder", "cleanroom",
    ):
        assert required in names
        d = describe(required)
        assert "package" in d


def test_kernel_call_development_info():
    k = NexusKernel().bootstrap()
    r = k.call("development", "info")
    assert r.ok, r.reason
    assert r.result["name"] == "development"


def test_kernel_call_simulation_list():
    k = NexusKernel().bootstrap()
    r = k.call("simulation", "list")
    assert r.ok, r.reason
    assert "nexus-party" in r.result["worlds"]


def test_kernel_unknown_pathway():
    k = NexusKernel().bootstrap()
    r = k.call("does-not-exist", "info")
    assert not r.ok


def test_call_uses_kernel_instances(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    k = NexusKernel().bootstrap()
    k.simulation.register("from-direct", kind="test")
    listed = k.call("simulation", "list")
    assert listed.ok, listed.reason
    assert "from-direct" in listed.result["worlds"]
    stored = k.call("memory", "put", "shared", {"n": 1})
    assert stored.ok, stored.reason
    assert k.memory.get("shared") == {"n": 1}


def test_declared_actions_allowed_undeclared_denied(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sample = tmp_path / "a.txt"
    sample.write_text("anchor", encoding="utf-8")
    k = NexusKernel().bootstrap()
    policy = k.call("security", "policy")
    assert policy.ok, policy.reason
    log = k.call("security", "log")
    assert log.ok, log.reason
    snap = k.call(
        "dashboard", "snapshot",
        subsystems={}, audit_len=0, security_log_len=0,
        memory_keys=0, experiments=0, adapter_status={},
    )
    assert snap.ok, snap.reason
    assert snap.result["claim"].startswith("local snapshot")
    tree = k.call("analysis", "analyze_tree", str(tmp_path))
    assert tree.ok, tree.reason
    assert tree.result["ok"] is True
    assigned = k.call("workforce", "assign", "engineer", "review layer0")
    assert assigned.ok, assigned.reason
    assert assigned.result["task"]["status"] == "pending"
    saved = k.call("integrity", "save_anchor", str(sample), "lbl")
    assert saved.ok, saved.reason
    assert saved.result["ok"] is True
    ran = k.call("runtime", "execute", "analyze repository", {"path": str(tmp_path)})
    assert ran.ok, ran.reason
    assert ran.result.success is True
    assert "list_files" in ran.result.steps
    denied = k.call("workforce", "deploy")
    assert denied.ok is False and denied.allowed is False
    query = k.call("cleanroom", "query", "x")
    assert query.ok is False and query.allowed is False
    assert "not declared" in query.reason


def test_user_facing_version_is_pyproject():
    from core.version import __version__
    root = __import__("pathlib").Path(__file__).resolve().parents[1]
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.3.2"' in pyproject
    assert __version__ == "0.3.2"
    k = NexusKernel().bootstrap()
    assert k.status()["version"] == "0.3.2"
    assert k.status()["version"] != "0.3.1"
