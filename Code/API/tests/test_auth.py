# tests/test_auth.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update with your actual base URL

@pytest.fixture
def user_data():
    return {
        "name": "Test User",
        "email": "user55@iitdh.ac.in",
        "password": "testpassword",
        "department": "Engineering",
        "userType": "Student",
        "phoneNumber": "1234567890"
    }

@pytest.fixture
def duplicate_user_data():
    return {
        "name": "Duplicate User",
        "email": "user52@iitdh.ac.in",
        "password": "testpassword",
        "department": "Engineering",
        "userType": "Student",
        "phoneNumber": "1234567890"
    }

def test_register_success(user_data):
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print("Register Success Status Code:", response.status_code)
    print("Register Success Response JSON:", response.json())
    assert response.status_code == 201
    assert "message" in response.json()
    assert response.json()["message"] == "User registered successfully"
    assert "user" in response.json()

def test_register_duplicate_user(duplicate_user_data):
    requests.post(f"{BASE_URL}/register", json=duplicate_user_data)  # Register once
    response = requests.post(f"{BASE_URL}/register", json=duplicate_user_data)  # Register again
    print("Duplicate Register Status Code:", response.status_code)
    print("Duplicate Register Response JSON:", response.json())
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_invalid_user_type(user_data):
    user_data["userType"] = "InvalidType"
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    print("Invalid UserType Status Code:", response.status_code)
    print("Invalid UserType Response JSON:", response.json())
    assert response.status_code == 400
    assert "error" in response.json()

def test_login_success(duplicate_user_data):
    requests.post(f"{BASE_URL}/register", json=duplicate_user_data)  # Ensure user is registered
    login_data = {
        "email": duplicate_user_data["email"],
        "password": duplicate_user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print("Login Success Status Code:", response.status_code)
    print("Login Success Response JSON:", response.json())
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Login successful"
    assert "user" in response.json()

def test_login_invalid_credentials(user_data):
    login_data = {
        "email": user_data["email"],
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print("Login Invalid Credentials Status Code:", response.status_code)
    print("Login Invalid Credentials Response JSON:", response.json())
    assert response.status_code == 401
    assert "message" in response.json()

def test_login_nonexistent_user():
    login_data = {
        "email": "nonexistent@iitdh.ac.in",
        "password": "somepassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print("Login Nonexistent User Status Code:", response.status_code)
    print("Login Nonexistent User Response JSON:", response.json())
    assert response.status_code == 401
    assert "message" in response.json()
