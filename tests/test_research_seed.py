"""CFT seeding is an explicit research action, not product bootstrap."""

import sys

from core.kernel import NexusKernel


def test_bootstrap_does_not_seed_cft_but_api_and_command_can(monkeypatch):
    import layer7_research.registry as research
    from core.nexus import main

    research._EXPERIMENTS.clear()
    NexusKernel().bootstrap()
    assert research.list_experiments() == []

    research.seed_cft_baseline()
    titles = {exp["title"] for exp in research.list_experiments()}
    assert "Ware Constant lock" in titles
    assert any(exp["source_repo"] == "ware-constant-phenomenology" for exp in research.list_experiments())

    research._EXPERIMENTS.clear()
    kernel = NexusKernel().bootstrap()
    assert research.list_experiments() == []
    seeded = kernel.call("research", "seed")
    assert seeded.ok, seeded.reason
    assert any(
        exp["source_repo"] == "ware-constant-phenomenology"
        for exp in research.list_experiments()
    )

    research._EXPERIMENTS.clear()
    monkeypatch.setattr(sys, "argv", ["core", "research"])
    assert main() == 0
    assert research.list_experiments() == []
    monkeypatch.setattr(sys, "argv", ["core", "research", "--seed"])
    assert main() == 0
    assert any(exp["title"] == "Ware Constant lock" for exp in research.list_experiments())
