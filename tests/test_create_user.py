import pytest
import allure
from tests.data import generate_user_data


@allure.feature("Создание пользователя")
class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api_client):
        with allure.step("Подготовка тестовых данных"):
            user_data = generate_user_data()

        with allure.step("Отправка запроса на создание"):
            response = api_client.create_user(user_data)
            response_data = response.json()

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert all(
                key in response_data for key in ['accessToken', 'refreshToken', 'user']), "Неполная структура ответа"

            user_info = response_data['user']
            assert user_info['email'] == user_data['email'], f"Email не совпадает. Ожидалось: {user_data['email']}"
            assert user_info['name'] == user_data['name'], f"Name не совпадает. Ожидалось: {user_data['name']}"
            assert isinstance(user_info['_id'], str), "ID пользователя должен быть строкой"
            assert '_v' in user_info, "Отсутствует версия документа"

    @allure.title("Создание существующего пользователя")
    def test_create_existing_user(self, api_client, test_user):
        with allure.step("Повторная регистрация пользователя"):
            response = api_client.create_user(test_user['data'])
            error_data = response.json()

        with allure.step("Проверка ошибки"):
            assert response.status_code == 403
            assert error_data['message'] == 'User already exists'
            assert error_data['status'] == 'error'
            assert 'accessToken' not in error_data, "Токен доступа не должен присутствовать при ошибке"
            assert 'user' not in error_data, "Данные пользователя не должны возвращаться"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize('field, expected_error', [
        ('email', 'Email is required'),
        ('password', 'Password is required'),
        ('name', 'Name is required')
    ])
    def test_create_user_missing_field(self, api_client, field, expected_error):
        with allure.step("Подготовка данных с пропущенным полем"):
            user_data = generate_user_data()
            del user_data[field]

        with allure.step("Отправка запроса"):
            response = api_client.create_user(user_data)
            error_data = response.json()

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400
            assert error_data['message'] == expected_error
            assert 'details' in error_data, "Должны быть детали ошибки"
            assert field in error_data['details'][0]['field'], f"Ошибка должна быть связана с полем {field}"

