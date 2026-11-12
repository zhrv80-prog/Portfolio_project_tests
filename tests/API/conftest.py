import pytest
import uuid
import requests
import os
import allure

REGISTER_ENDPOINT = '/users'
LOGIN_ENDPOINT = '/users/login'
DELETE_ENDPOINT = '/users/{id}'


@pytest.fixture
def api_url():
    """Базовый URL API."""
    return 'https://thinking-tester-contact-list.herokuapp.com'


@pytest.fixture
def user_password():
    """Пароль для тестового пользователя из переменной окружения."""
    password = os.getenv("MY_APP_PASSWORD")
    assert password is not None, "MY_APP_PASSWORD is not set"
    return password


@pytest.fixture
def user(api_url, user_password):
    """
    Создаёт пользователя и удаляет его после теста.
    Возвращает словарь с id, email, payload и password.
    """
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

    created = response.json()["user"]

    yield {
        "id": created["_id"],
        "email": email,
        "password": user_password,
        "payload": payload,
    }

    # --- TEARDOWN: delete user ---
    with allure.step(f"DELETE user {email}"):
        try:
            # Логинимся, чтобы получить токен для удаления
            login_response = requests.post(
                f"{api_url}{LOGIN_ENDPOINT}",
                json={"email": email, "password": user_password}
            )
            if login_response.status_code == 200:
                token = login_response.json()["token"]
                requests.delete(
                    f"{api_url}{DELETE_ENDPOINT.format(id=created['_id'])}",
                    headers={"Authorization": f"Bearer {token}"}
                )
            else:
                print(f"Warning: Login failed for {email}, cannot delete user")
        except Exception as e:
            print(f"Warning: Failed to delete user {email}: {e}")


@pytest.fixture
def auth_token(user, api_url):
    """
    Логинит созданного пользователя и возвращает токен.
    Зависит от фикстуры `user`.
    """
    with allure.step(f"POST {LOGIN_ENDPOINT} for {user['email']}"):
        response = requests.post(
            f"{api_url}{LOGIN_ENDPOINT}",
            json={"email": user["email"], "password": user["password"]}
        )

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}. Body: {response.text}"
        )

    token = response.json()["token"]
    return token