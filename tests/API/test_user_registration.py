import time

import allure
import requests
import os


@allure.feature("User Registration")
@allure.story("Successful registration with valid data")
def test_user_registration(created_user):
    created_user
