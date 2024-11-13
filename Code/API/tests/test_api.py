import pytest
import requests
import random
import string

BASE_URL = "http://127.0.0.1:5000"  # Update with your actual base URL

@pytest.fixture
def random_email():
    """Generate a random email for testing."""
    return f"user_{random.randint(1, 10000)}@iitdh.ac.in"

@pytest.fixture
def user_data(random_email):
    """Fixture to provide user data for registration."""
    return {
        "name": "Test User",
        "email": random_email,
        "password": "Password123!",
        "department": "Engineering",
        "userType": "Student",
        "phoneNumber": "1234567890"
    }

@pytest.fixture
def login_data(user_data):
    """Fixture to provide login data from user data."""
    return {
        "email": user_data["email"],
        "password": user_data["password"]
    }

def test_register_success(user_data):
    """Test successful registration of a user."""
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 201
    assert "message" in response.json()
    assert response.json()["message"] == "User registered successfully"
    assert "user" in response.json()

def test_register_duplicate_user(user_data):
    """Test registration of a duplicate user."""
    requests.post(f"{BASE_URL}/register", json=user_data)  # Register once
    response = requests.post(f"{BASE_URL}/register", json=user_data)  # Register again
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_invalid_user_type(user_data):
    """Test registration with an invalid user type."""
    user_data["userType"] = "InvalidType"
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_invalid_email_format(user_data):
    """Test registration with an invalid email format."""
    user_data["email"] = "invalid-email-format"
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_short_password(user_data):
    """Test registration with a short password."""
    user_data["password"] = "short"
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_duplicate_phone_number(user_data):
    """Test registration with a duplicate phone number."""
    requests.post(f"{BASE_URL}/register", json=user_data)  # Register once
    user_data["email"] = f"unique_{random.randint(10000, 99999)}@iitdh.ac.in"  # Change email to make it unique
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_case_insensitive_email(user_data):
    """Test case-insensitive email registration."""
    requests.post(f"{BASE_URL}/register", json=user_data)  # Register once
    user_data["email"] = user_data["email"].upper()  # Change to uppercase to test case sensitivity
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_register_missing_fields(user_data):
    """Test registration with missing fields."""
    for key in user_data:
        incomplete_data = user_data.copy()
        del incomplete_data[key]
        response = requests.post(f"{BASE_URL}/register", json=incomplete_data)
        assert response.status_code == 400
        assert "error" in response.json()

def test_login_success(login_data, user_data):
    """Test successful login."""
    requests.post(f"{BASE_URL}/register", json=user_data)  # Ensure user is registered
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Login successful"
    assert "user" in response.json()

def test_login_invalid_credentials(user_data):
    """Test login with invalid credentials."""
    login_data = {
        "email": user_data["email"],
        "password": "WrongPassword!"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 401
    assert "message" in response.json()

def test_login_nonexistent_user():
    """Test login with a nonexistent user."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "SomePassword!"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 401
    assert "message" in response.json()

def test_login_missing_fields():
    """Test login with missing fields."""
    login_data = {
        "email": "nonexistent@iitdh.ac.in",
        "password": "somepassword"
    }
    for field in login_data.keys():
        incomplete_data = login_data.copy()
        incomplete_data.pop(field)
        response = requests.post(f"{BASE_URL}/login", json=incomplete_data)
        assert response.status_code == 400
        assert "error" in response.json()

def test_login_invalid_email_format(user_data):
    """Test login with an invalid email format."""
    login_data = {
        "email": "invalid-email-format",
        "password": user_data["password"]
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 401
    assert "message" in response.json()

def test_register_multiple_users(user_data):
    """Test registration of multiple unique users."""
    for i in range(3):
        user_data["email"] = f"user_{random.randint(10000, 99999)}@iitdh.ac.in"  # Generate unique email
        response = requests.post(f"{BASE_URL}/register", json=user_data)
        assert response.status_code == 201
        assert "message" in response.json()
        assert response.json()["message"] == "User registered successfully"
        assert "user" in response.json()
