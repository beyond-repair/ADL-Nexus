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

def test_unknown_action_heuristic_denies_cleanroom_query():
    from layer5_security.gate import POLICY
    assert "query" not in POLICY["allow"]
    g = SecurityGate(min_trust=0.5)
    d = g.evaluate("cleanroom-adapter", "query")
    assert d.allowed is False
    assert d.trust_score == 0.25
    assert d.policy_match == "heuristic"
    assert "0.25" in d.reason
