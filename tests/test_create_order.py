import pytest
import allure


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized(self, api_client, test_user):
        with allure.step("Получение списка ингредиентов"):
            ingredients = api_client.get_ingredients().json()['data']
            valid_ingredients = [ingredient['_id'] for ingredient in ingredients[:2]]

        with allure.step("Создание заказа"):
            response = api_client.create_order(
                ingredients=valid_ingredients,
                token=test_user['response'].json()['accessToken']
            )

        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert response.json()['order']['number'] is not None

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, api_client):
        with allure.step("Получение ингредиентов"):
            ingredients = api_client.get_ingredients().json()['data']
            valid_ingredients = [ingredient['_id'] for ingredient in ingredients[:2]]

        with allure.step("Создание заказа без токена"):
            response = api_client.create_order(ingredients=valid_ingredients)

        with allure.step("Проверка ответа"):
            assert response.status_code == 200

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_hash(self, api_client, test_user):
        with allure.step("Использование невалидных ингредиентов"):
            response = api_client.create_order(
                ingredients=['invalid_hash1', 'invalid_hash2'],
                token=test_user['response'].json()['accessToken']
            )

        with allure.step("Проверка ошибки"):
            assert response.status_code == 500
