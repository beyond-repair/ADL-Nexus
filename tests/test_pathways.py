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
