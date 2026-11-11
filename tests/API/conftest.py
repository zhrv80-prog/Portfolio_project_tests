import pytest
import uuid
import requests
import os
import allure

REGISTER_ENDPOINT = '/users'
DELETE_ENDPOINT = '/users/{id}'


@pytest.fixture
def api_url():
    return 'https://thinking-tester-contact-list.herokuapp.com'


@pytest.fixture
def user_password():
    password = os.getenv("MY_APP_PASSWORD")
    assert password is not None, "MY_APP_PASSWORD is not set"
    return password


@pytest.fixture
def created_user(api_url, user_password):
    # --- SETUP: create user ---
    email = f"testuser{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "firstName": "Test",
        "lastName": "User",
        "email": email,
        "password": user_password,
    }

    with allure.step(f"POST {REGISTER_ENDPOINT} with email={email}"):
        response = requests.post(f"{api_url}{REGISTER_ENDPOINT}", json=payload)

    with allure.step("Verify status code is 201"):
        assert response.status_code == 201, (
            f"Expected 201, got {response.status_code}. Body: {response.text}"
        )

    with allure.step("Verify response contains expected user data"):
        body = response.json()
        assert body.get("user", {}).get("email") == email
        assert body.get("user", {}).get("firstName") == "Test"
        assert body.get("user", {}).get("lastName") == "User"
        assert "password" not in body.get("user", {})

    user = response.json()["user"]

    yield {"id": user["_id"], "email": email, "payload": payload}

    # --- TEARDOWN: delete user ---
    with allure.step(f"DELETE user {email}"):
        try:
            requests.delete(f"{api_url}{DELETE_ENDPOINT.format(id=user['_id'])}")
        except Exception as e:
            print(f"Warning: Failed to delete user {email}: {e}")