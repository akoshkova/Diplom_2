import random
import string

def generate_user_data():
    return {
        "email": f"test_{random_string(6)}@example.com",
        "password": random_string(10),
        "name": random_string(8)
    }

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def existing_user_data():
    return {
        "email": "existing@user.com",
        "password": "password123",
        "name": "Existing User"
    }

def invalid_user_data():
    return {
        "email": "invalid@user.com",
        "password": "short"
    }

def invalid_login_data():
    return {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }

