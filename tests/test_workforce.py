from layer3_workforce.roles import list_roles, get_role

def test_roles_exist():
    roles = list_roles()
    assert "engineer" in roles
    assert "researcher" in roles
    r = get_role("engineer")
    assert "code" in r.capabilities
