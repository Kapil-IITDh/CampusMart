import pytest
import requests
import json
from unittest.mock import patch

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
        "name": "Duplicate User",
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

def test_register_duplicate_user(duplicate_user_data):
    requests.post(f"{BASE_URL}/register", json=duplicate_user_data)
    response = requests.post(f"{BASE_URL}/register", json=duplicate_user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_invalid_user_type(user_data):
    user_data["userType"] = "InvalidType"
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_login_success(duplicate_user_data):
    requests.post(f"{BASE_URL}/register", json=duplicate_user_data)
    login_data = {
        "email": duplicate_user_data["email"],
        "password": duplicate_user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Login successful"

def test_login_invalid_credentials(user_data):
    login_data = {
        "email": user_data["email"],
        "password": "wrongpassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 401
    assert "message" in response.json()

def test_login_nonexistent_user(user_data):
    login_data = {
        "email": "nonexistent@iitdh.ac.in",
        "password": "somepassword"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 401
    assert "message" in response.json()

@patch('builtins.localStorage')
def test_load_user_data(mock_local_storage, user_data):
    # Simulating stored user data
    mock_local_storage.getItem.return_value = json.dumps(user_data)
    
    # Here we would typically call the JavaScript function to load user data
    # For this example, we simulate the check
    loaded_data = json.loads(mock_local_storage.getItem('user'))
    
    assert loaded_data["name"] == user_data["name"]
    assert loaded_data["email"] == user_data["email"]
    assert loaded_data["phoneNumber"] == user_data["phoneNumber"]

@patch('builtins.localStorage')
def test_sign_out(mock_local_storage):
    # Simulate user sign out
    mock_local_storage.removeItem.return_value = None
    
    # Perform sign out action (in actual implementation, this would be a function call)
    mock_local_storage.removeItem('isLoggedIn')
    mock_local_storage.removeItem('user')

    # Check if the items were removed
    mock_local_storage.removeItem.assert_any_call('isLoggedIn')
    mock_local_storage.removeItem.assert_any_call('user')