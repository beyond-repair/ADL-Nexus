from layer5_security.gate import SecurityGate

def test_security_allows_safe_actions():
    g = SecurityGate(min_trust=0.5)
    d = g.evaluate("coding-agent", "list_files")
    assert d.allowed
    assert d.policy_match == "allow"

def test_security_blocks_denied():
    g = SecurityGate(min_trust=0.5)
    d = g.evaluate("coding-agent", "exfiltrate")
    assert not d.allowed
    assert d.policy_match == "deny"

def test_security_blocks_elevated_unknown():
    g = SecurityGate(min_trust=0.5)
    d = g.evaluate("coding-agent", "weird_action", {"elevated": True})
    assert not d.allowed
