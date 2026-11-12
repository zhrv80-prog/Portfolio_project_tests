import allure
import requests


def test_delete_user(user, api_url):
    """Проверяет удаление пользователя."""
    with allure.step("DELETE /users/me"):
        response = requests.delete(
            f"{api_url}/users/me",
            headers={"Authorization": f"Bearer {user['token']}"}
        )

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify user is deleted"):
        check = requests.get(
            f"{api_url}/users/me",
            headers={"Authorization": f"Bearer {user['token']}"}
        )
        assert check.status_code == 401