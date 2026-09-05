"""Basic governance tests."""

from layer0_governance.registry import register_subsystem, evaluate_request, list_subsystems

def test_register_and_evaluate():
    h = register_subsystem("test-sub", layer=2, claim_level=1, capabilities=["ping"])
    assert h
    assert "test-sub" in list_subsystems()
    d = evaluate_request("test-sub", "ping")
    assert d.allowed
    d2 = evaluate_request("test-sub", "forbidden")
    assert not d2.allowed
