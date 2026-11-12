def test_create_user(user):
    """Assert that user is created successfully"""
    assert user["email"] is not None
    assert user["id"] is not None