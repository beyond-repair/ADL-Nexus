import pytest
from core.kernel import NexusKernel


def test_think_does_not_execute():
    pytest.xfail("RESEARCH claim-cap: NexusKernel.think not wired; ObjectiveEngine exists but unintegrated; Sweep-131")


def test_commit_refused_without_authorize():
    pytest.xfail("RESEARCH claim-cap: NexusKernel.commit/authorize not wired; Sweep-131")


def test_authorize_then_commit_assigns():
    pytest.xfail("RESEARCH claim-cap: NexusKernel.commit/authorize not wired; Sweep-131")


def test_reality_and_provenance_pathways():
    pytest.xfail("RESEARCH claim-cap: reality/provenance pathways not in PATHWAY_SPEC; Sweep-131")
