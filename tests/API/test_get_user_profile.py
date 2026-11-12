import allure
import requests


def test_get_user_info(user, api_url):
    """Проверяет получение информации о пользователе."""
    with allure.step("GET /users/me"):
        response = requests.get(
            f"{api_url}/users/me",
            headers={"Authorization": f"Bearer {user['token']}"}
        )

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify user data"):
        body = response.json()
        assert body["email"] == user["user"].email
        assert body["firstName"] == user["user"].firstName
        assert body["lastName"] == user["user"].lastName
        assert "password" not in body