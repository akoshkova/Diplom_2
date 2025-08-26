import pytest
import allure
from tests.data import generate_user_data


@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.title("Успешный вход существующего пользователя")
    def test_login_valid_user(self, api_client, test_user):
        with allure.step("Отправка валидных данных"):
            response = api_client.login_user({
                "email": test_user['data']['email'],
                "password": test_user['data']['password']
            })

        with allure.step("Проверка успешной авторизации"):
            assert response.status_code == 200
            assert 'accessToken' in response.json()

    @allure.title("Вход с неверными данными")
    def test_login_invalid_credentials(self, api_client):
        with allure.step("Отправка неверных данных"):
            response = api_client.login_user({
                "email": "invalid@example.com",
                "password": "wrongpassword"
            })

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            assert response.json()['message'] == 'email or password are incorrect'
