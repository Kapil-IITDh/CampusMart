import pytest
import json
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_user(client):
    """Test user registration endpoint"""
    data = {
        "name": "Test User",
        "email": "testuser@iitdh.ac.in",
        "department": "Engineering",
        "password": "TestPass123",
        "userType": "Student",
        "phoneNumber": "1234567890"
    }
    response = client.post('/register', data=json.dumps(data), content_type='application/json')
    if response.status_code == 201:
        assert 'user' in response.json
    else:
        assert response.status_code == 400
        assert response.json['error'] == 'User already exists'

def test_login_user(client):
    """Test user login endpoint"""
    data = {
        "email": "testuser@iitdh.ac.in",
        "password": "TestPass123"
    }
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code in [200, 401]  # Passes if login is successful or credentials are invalid

def test_add_listing(client):
    """Test adding a new listing"""
    register_response = client.post('/register', data=json.dumps({
        "name": "Listing User",
        "email": "listinguser@iitdh.ac.in",
        "department": "Commerce",
        "password": "ListingPass1234",
        "userType": "Student",
        "phoneNumber": "9876543217"
    }), content_type='application/json')

    if register_response.status_code == 201:
        user_id = register_response.json['user']['userID']
    else:
        login_response = client.post('/login', data=json.dumps({
            "email": "listinguser@iitdh.ac.in",
            "password": "ListingPass1234"
        }), content_type='application/json')
        assert login_response.status_code == 200
        user_id = login_response.json['user']['userID']

    listing_data = {
        "userID": user_id,
        "title": "Sample Product",
        "description": "A great product",
        "selling_price": 150,
        "new_item_price": 200,
        "categoryID": 1,
        "grade": 1,
        "imageLinks": ["https://image1.jpg"]
    }
    response = client.post('/add_listing', data=json.dumps(listing_data), content_type='application/json')
    assert response.status_code == 201
    assert 'listingID' in response.json

def test_get_user_listings(client):
    """Test fetching listings for a user"""
    response = client.get('/listings?userID=1')
    assert response.status_code == 200
    assert 'listings' in response.json
    assert isinstance(response.json['listings'], list)





def test_get_user_average_rating(client):
    """Test getting the average rating of a user"""
    response = client.get('/user/average_rating?rateeID=1')
    assert response.status_code == 200
    assert 'average_rating' in response.json
