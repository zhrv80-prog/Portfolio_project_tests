import pytest
import uuid
import requests
import os
import allure

from basemodels.user.user_models import User
# from dataclasses import dataclass, asdict
#
#
# # --- Модель данных ---
# @dataclass
# class User:
#     firstName: str
#     lastName: str
#     email: str
#     password: str
#
#     def to_dict(self) -> dict:
#         return asdict(self)


# --- Эндпоинты ---
REGISTER_ENDPOINT = '/users'
DELETE_ENDPOINT = '/users/me'


# --- Фикстуры ---
@pytest.fixture
def user_password():
    password = os.getenv("MY_APP_PASSWORD")
    assert password is not None, "MY_APP_PASSWORD is not set"
    return password


@pytest.fixture
def api_url():
    return "https://thinking-tester-contact-list.herokuapp.com"


@pytest.fixture
def user(api_url, user_password):
    # --- SETUP: create user ---
    email = f"testuser{uuid.uuid4().hex[:8]}@example.com"

    user = User(
        firstName="Marcus",
        lastName="William",
        email=email,
        password=user_password,
    )

    with allure.step(f"POST {REGISTER_ENDPOINT} with email={email}"):
        response = requests.post(
            f"{api_url}{REGISTER_ENDPOINT}",
            json=user.to_dict()
        )
    assert response.status_code == 201, f"Create failed: {response.text}"

    body = response.json()
    token = body["token"]

    yield {
        "email": user.email,
        "token": token,
        "user": user,  # ← передаём сам dataclass
    }

    # --- TEARDOWN: delete user ---
    with allure.step(f"DELETE {DELETE_ENDPOINT}"):
        try:
            requests.delete(
                f"{api_url}{DELETE_ENDPOINT}",
                headers={"Authorization": f"Bearer {token}"}
            )
        except Exception as e:
            print(f"Warning: Failed to delete user {user.email}: {e}")