import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_user(self, data):
        return requests.post(f'{self.base_url}/auth/register', json=data)

    def login_user(self, data):
        return requests.post(f'{self.base_url}/auth/login', json=data)

    def delete_user(self, token):
        return requests.delete(f'{self.base_url}/auth/user', headers={'Authorization': token})

    def create_order(self, ingredients, token=None):
        headers = {'Authorization': token} if token else {}
        return requests.post(f'{self.base_url}/orders', json={'ingredients': ingredients}, headers=headers)

    def get_ingredients(self):
        return requests.get(f'{self.base_url}/ingredients')
