import allure
import requests


def test_delete_user(user, auth_token, api_url):
    """Проверяет удаление пользователя."""
    with allure.step(f"DELETE /users/{user['id']}"):
        response = requests.delete(
            f"{api_url}/users/{user['id']}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify user is deleted"):
        check = requests.get(
            f"{api_url}/users/{user['id']}",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert check.status_code == 401  # или 404, зависит от API