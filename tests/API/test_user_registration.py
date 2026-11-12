import time

import allure
import requests
import os


@allure.feature("User Registration")
@allure.story("Successful registration with valid data")
def test_user_registration(user_lifecycle):
    assert user_lifecycle["email"] is not None
    assert user_lifecycle["id"] is not None
