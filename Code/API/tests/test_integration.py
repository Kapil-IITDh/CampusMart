# tests/test_integration.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update with your actual base URL

@pytest.fixture
def user_data():
    """Fixture to provide user data for registration."""
    return {
        "name": "Integration Test User",
        "email": "integration_user@example.com",
        "password": "Password123!",
        "department": "Computer Science",
        "userType": "Student",
        "phoneNumber": "1234567890"
    }

@pytest.fixture
def login_data(user_data):
    """Fixture to provide login data."""
    return {
        "email": user_data["email"],
        "password": user_data["password"]
    }

@pytest.fixture
def authenticated_session(login_data, user_data):
    """Fixture to create an authenticated session."""
    # Register the user first
    requests.post(f"{BASE_URL}/register", json=user_data)
    # Login to get a token
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    token = response.json().get("token")
    return token

def test_user_registration_and_login(user_data, login_data):
    """Test user registration followed by login."""
    # Register the user
    response = requests.post(f"{BASE_URL}/register", json=user_data)
    assert response.status_code == 201
    assert response.json().get("message") == "User registered successfully"

    # Attempt to log in
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    assert response.status_code == 200
    assert "token" in response.json()  # Expecting a token on successful login

def test_create_listing(authenticated_session):
    """Test creating a listing as an authenticated user."""
    listing_data = {
        "userID": 1,  # Use a valid user ID from your database
        "title": "Test Listing",
        "description": "This is a test listing.",
        "selling_price": 50.0,
        "new_item_price": 75.0,
        "categoryID": 1,  # Use a valid category ID
        "grade": "New"
    }
    
    response = requests.post(f"{BASE_URL}/product", json=listing_data, headers={"Authorization": f"Bearer {authenticated_session}"})
    assert response.status_code == 201
    assert response.json().get("message") == "Product added successfully"

def test_get_products():
    """Test fetching all products."""
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200
    assert isinstance(response.json().get("products"), list)  # Expecting a list of products

def test_get_user_profile(authenticated_session):
    """Test fetching user profile data."""
    response = requests.get(f"{BASE_URL}/users/1", headers={"Authorization": f"Bearer {authenticated_session}"})  # Use a valid user ID
    assert response.status_code == 200
    assert "email" in response.json()  # Check if email is part of the response

def test_user_logout(authenticated_session):
    """Test user logout (simulated by not using the token)."""
    # Since the logout isn't implemented in the API, we'll just test that the session works.
    response = requests.get(f"{BASE_URL}/some_protected_route", headers={"Authorization": f"Bearer {authenticated_session}"})
    assert response.status_code == 200  # Assuming this route requires authentication
