# tests/test_orders.py

import pytest
import requests

BASE_URL = "http://127.0.0.1:5000"  # Ensure this points to your app

@pytest.fixture
def product_data():
    """Sample product data for testing."""
    return {
        "userID": 1,
        "title": "Test Product",
        "description": "Test product description",
        "selling_price": 1000.00,
        "new_item_price": 1200.00,
        "categoryID": 1,
        "grade": 4
    }

def test_create_product(product_data):
    """Test successful product creation."""
    response = requests.post(f"{BASE_URL}/product", json=product_data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code} with response: {response.text}"
    assert response.json().get("message") == "Product added successfully"

def test_get_all_products():
    """Test fetching all products."""
    response = requests.get(f"{BASE_URL}/products")
    assert response.status_code == 200, f"Expected 200, got {response.status_code} with response: {response.text}"
    assert isinstance(response.json().get("products"), list)  # Expecting a list of products

def test_add_to_wishlist():
    """Test adding a product to the wishlist."""
    wishlist_data = {"userID": 2, "listingID": 11}
    response = requests.post(f"{BASE_URL}/wishlist", json=wishlist_data)
    assert response.status_code == 201, f"Expected 201, got {response.status_code} with response: {response.text}"
    assert response.json().get("message") == "Product added to wishlist successfully"
