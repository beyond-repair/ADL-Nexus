from layer5_security.gate import SecurityGate

def test_security_allows_safe_actions():
    g = SecurityGate(min_trust=0.5)
    d = g.evaluate("coding-agent", "list_files")
    assert d.allowed
    assert d.trust_score >= 0.5

def test_security_blocks_elevated():
    g = SecurityGate(min_trust=0.5)
    d = g.evaluate("coding-agent", "dangerous", {"elevated": True})
    assert not d.allowed
