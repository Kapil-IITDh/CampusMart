# tests/test_auth.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update with your actual base URL

@pytest.fixture
def user_data():
    return {
        "name": "Test User",
        "email": "testuser@iitdh.ac.in",
        "password": "testpassword",
        "department": "Engineering",
        "userType": "Student",
        "phoneNumber": "1234567890"
    }

@pytest.fixture
def duplicate_user_data():
    return {
        "name": "Test User",
        "email": "duplicateuser@iitdh.ac.in",
        "password": "testpassword",
        "department": "Engineering",
        "userType": "Student",
        "phoneNumber": "1234567890"
    }

def test_register_success(user_data):
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 201
    assert "message" in response.json()
    assert response.json()["message"] == "User registered successfully"
    assert "user" in response.json()

def test_register_duplicate_user(duplicate_user_data):
    # First, register the user
    requests.post(f"{BASE_URL}/register", json=duplicate_user_data)

    # Attempt to register again
    response = requests.post(f"{BASE_URL}/register", json=duplicate_user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_invalid_user_type(user_data):
    user_data["userType"] = "InvalidType"
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_login_success(duplicate_user_data):
    # First, register the user
    requests.post(f"{BASE_URL}/register", json=duplicate_user_data)

    # Attempt to log in
    login_data = {
        "email": duplicate_user_data["email"],
        "password": duplicate_user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Login successful"
    assert "user" in response.json()

def test_login_invalid_credentials(user_data):
    # Attempt to log in with invalid credentials
    login_data = {
        "email": user_data["email"],
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 401
    assert "message" in response.json()

def test_login_nonexistent_user(user_data):
    # Attempt to log in with a nonexistent user
    login_data = {
        "email": "nonexistent@iitdh.ac.in",
        "password": "somepassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 401
    assert "message" in response.json()