import pytest
import allure
from tests.data import generate_user_data, existing_user_data, invalid_user_data


@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api_client):
        with allure.step("Подготовка тестовых данных"):
            user_data = generate_user_data()

        with allure.step("Отправка запроса на создание"):
            response = api_client.create_user(user_data)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert 'accessToken' in response.json()

    @allure.title("Создание существующего пользователя")
    def test_create_existing_user(self, api_client, test_user):
        with allure.step("Повторная регистрация пользователя"):
            response = api_client.create_user(test_user['data'])

        with allure.step("Проверка ошибки"):
            assert response.status_code == 403
            assert response.json()['message'] == 'User already exists'

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize('field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, api_client, field):
        with allure.step("Подготовка данных с пропущенным полем"):
            user_data = generate_user_data()
            del user_data[field]

        with allure.step("Отправка запроса"):
            response = api_client.create_user(user_data)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 403
            assert response.json()['message'] == 'Email, password and name are required fields'
