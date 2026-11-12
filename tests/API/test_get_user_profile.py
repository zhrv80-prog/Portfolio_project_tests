import allure
import requests


def test_get_user_info(user, auth_token, api_url):
    """Get user info"""
    with allure.step(f"GET /users/me with token"):
        response = requests.get(
            f"{api_url}/users/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

    with allure.step("Verify status code is 200"):
        assert response.status_code == 200

    with allure.step("Verify user data"):
        body = response.json()
        assert body["email"] == user["email"]
        assert body["firstName"] == "Test"
        assert body["lastName"] == "User"
        assert "password" not in body