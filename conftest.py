import pytest
import allure
from utils.api_client import ApiClient
from tests.data import generate_user_data

@pytest.fixture(scope='function')
def api_client():
    return ApiClient(base_url='https://stellarburgers.nomoreparties.site/api')

@pytest.fixture(scope='function')
def test_user(api_client):
    user_data = generate_user_data()
    response = api_client.create_user(user_data)
    yield {'data': user_data, 'response': response}
    api_client.delete_user(response.json()['accessToken'])
