"""Basic governance tests."""

import pytest

from layer0_governance.registry import register_subsystem, evaluate_request, list_subsystems
from layer0_governance import registry as registry_mod


def test_register_and_evaluate():
    h = register_subsystem("test-sub", layer=2, claim_level=1, capabilities=["ping"])
    assert h
    assert "test-sub" in list_subsystems()
    d = evaluate_request("test-sub", "ping")
    assert d.allowed
    d2 = evaluate_request("test-sub", "forbidden")
    assert not d2.allowed


def test_claim_level_above_cap_fails_closed():
    with pytest.raises(ValueError, match="exceeds cap"):
        register_subsystem("elev", layer=0, claim_level=9, capabilities=["ping"])
    assert "elev" not in list_subsystems()
    missing = evaluate_request("elev", "ping")
    assert missing.allowed is False

    registry_mod._REGISTRY["elev"] = {
        "name": "elev",
        "layer": 0,
        "claim_level": 9,
        "capabilities": ["ping"],
        "reg_hash": "x",
    }
    try:
        denied = evaluate_request("elev", "ping")
        assert denied.allowed is False
        assert "exceeds cap" in denied.reason
        status = evaluate_request("elev", "status")
        assert status.allowed is False
        assert "exceeds cap" in status.reason
    finally:
        registry_mod._REGISTRY.pop("elev", None)


def test_claim_at_cap_allowed_and_self_elevate_refused():
    h = register_subsystem("at-cap", layer=1, claim_level=2, capabilities=["ping"])
    assert h
    assert evaluate_request("at-cap", "ping").allowed is True
    register_subsystem("low-claim", layer=1, claim_level=1, capabilities=["ping"])
    with pytest.raises(ValueError, match="self-elevate"):
        register_subsystem("low-claim", layer=1, claim_level=2, capabilities=["ping"])
    assert list_subsystems()["low-claim"]["claim_level"] == 1
