# tests/test_orders.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Update with your actual base URL

@pytest.fixture
def order_data():
    """Fixture to provide order data for testing."""
    return {
        "productId": 1,  # Assume product with ID 1 exists
        "quantity": 1
    }

@pytest.fixture
def access_token():
    """Dummy access token for testing."""
    return "dummy_token"  # Replace with valid token logic as needed

def test_create_order_success(order_data, access_token):
    """Test successful order creation."""
    response = requests.post(f"{BASE_URL}/orders", json=order_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 201
    assert response.json().get("message") == "Order created successfully"

def test_create_order_invalid_product(order_data, access_token):
    """Test order creation with an invalid product ID."""
    order_data["productId"] = 9999  # Assume this product ID doesn't exist
    response = requests.post(f"{BASE_URL}/orders", json=order_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 400
    assert "error" in response.json()

def test_get_order_history(access_token):
    """Test retrieving the user's order history."""
    response = requests.get(f"{BASE_URL}/orders/history", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of orders
