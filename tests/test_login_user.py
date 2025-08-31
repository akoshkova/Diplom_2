import pytest
import allure
from tests.data import existing_user_data, invalid_login_data


@allure.feature("Логин пользователя")
class TestLoginUser:
    @allure.title("Успешный вход существующего пользователя")
    def test_login_valid_user(self, api_client, test_user):
        with allure.step("Отправка валидных данных"):
            response = api_client.login_user({
                "email": existing_user_data()['email'],
                "password": existing_user_data()['password']
            })
            response_data = response.json()

        with allure.step("Проверка успешной авторизации"):
            # Проверка статуса и структуры ответа
            assert response.status_code == 200, "Ожидался код 200 при успешной авторизации"

            # Проверка наличия обязательных полей
            assert all(key in response_data for key in ['accessToken', 'refreshToken', 'user']), \
                "В ответе отсутствуют обязательные поля"

            # Проверка данных пользователя
            user_info = response_data['user']
            assert user_info['email'] == existing_user_data()['email'], "Email не совпадает"
            assert user_info['name'] == existing_user_data()['name'], "Имя не совпадает"
            assert isinstance(user_info['_id'], str), "ID пользователя должен быть строкой"

    @allure.title("Вход с неверными данными")
    def test_login_invalid_credentials(self, api_client):
        with allure.step("Отправка неверных данных"):
            invalid_data = invalid_login_data()
            response = api_client.login_user(invalid_data)
            error_data = response.json()

        with allure.step("Проверка ошибки авторизации"):
            # Проверка статуса и структуры ошибки
            assert response.status_code == 401, "Ожидался код 401 при неверных данных"
            assert 'message' in error_data, "Отсутствует сообщение об ошибке"

            # Проверка содержимого ошибки
            assert error_data['message'] == 'email or password are incorrect', \
                "Неверное сообщение об ошибке"

            # Проверка отсутствия токенов
            assert 'accessToken' not in error_data, "Токен доступа не должен присутствовать"
            assert 'user' not in error_data, "Данные пользователя не должны возвращаться"

    @allure.title("Вход с неполными данными")
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_login_missing_fields(self, api_client, missing_field):
        with allure.step("Подготовка данных с пропущенным полем"):
            test_data = {k: v for k, v in existing_user_data().items() if k != missing_field}

        with allure.step("Отправка неполных данных"):
            response = api_client.login_user(test_data)
            error_data = response.json()

        with allure.step("Проверка ошибки"):
            assert response.status_code == 400, "Ожидался код 400 при неполных данных"
            assert 'message' in error_data, "Отсутствует сообщение об ошибке"
            assert error_data['message'] == f'{missing_field.capitalize()} is required', \
                "Неверное сообщение об ошибке"


