import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


from ..app import app, get_db_connection  # Adjusted import statement
import unittest
import pytest
from flask import json

@pytest.fixture
class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, welcome to CampusMart API!', response.get_json()['message'])

    def test_get_user(self):
        response = self.client.get('/users/1')
        if response.status_code == 200:
            self.assertIn('userID', response.get_json())
        else:
            self.assertEqual(response.status_code, 404)

    def test_register(self):
        data = {
            "name": "Test User",
            "email": "testuser@example.com",
            "department": "CSE",
            "password": "password123",
            "userType": "Student",
            "phoneNumber": "1234567890"
        }
        response = self.client.post('/register', data=json.dumps(data), content_type='application/json')
        self.assertIn(response.status_code, [201, 400])

    def test_login(self):
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = self.client.post('/login', data=json.dumps(data), content_type='application/json')
        self.assertIn(response.status_code, [200, 401])

    def test_get_all_categories(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)

    def test_get_category(self):
        response = self.client.get('/categories/1')
        if response.status_code == 200:
            self.assertIn('categoryID', response.get_json())
        else:
            self.assertEqual(response.status_code, 404)

    def test_get_products(self):
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)

    def test_get_product(self):
        response = self.client.get('/products/1')
        if response.status_code == 200:
            self.assertIn('listingID', response.get_json())
        else:
            self.assertEqual(response.status_code, 404)

    def test_add_product(self):
        data = {
            "userID": 1,
            "title": "New Product",
            "description": "This is a test product",
            "selling_price": 100,
            "new_item_price": 150,
            "categoryID": 1,
            "grade": "A"
        }
        response = self.client.post('/product', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_update_product(self):
        data = {
            "title": "Updated Product",
            "description": "Updated description",
            "selling_price": 120,
            "new_item_price": 170,
            "categoryID": 1,
            "grade": "A"
        }
        response = self.client.put('/product/1', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        response = self.client.delete('/product/1')
        self.assertEqual(response.status_code, 200)

    def test_get_listing_images(self):
        response = self.client.get('/listing_images')
        self.assertEqual(response.status_code, 200)

    def test_get_all_messages(self):
        response = self.client.get('/messages/1')
        self.assertEqual(response.status_code, 200)

    def test_send_message(self):
        data = {
            "sender_id": 1,
            "receiver_id": 2,
            "message": "Hello"
        }
        response = self.client.post('/message', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_chatted_users(self):
        response = self.client.get('/users/1/chats')
        self.assertEqual(response.status_code, 200)

    def test_get_all_ratings(self):
        response = self.client.get('/ratings')
        self.assertEqual(response.status_code, 200)

    def test_add_rating(self):
        data = {
            "listingID": 1,
            "userID": 1,
            "ratingValue": 4
        }
        response = self.client.post('/rating', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_all_transactions(self):
        response = self.client.get('/transactions')
        self.assertEqual(response.status_code, 200)

    def test_add_transaction(self):
        data = {
            "buyerID": 1,
            "sellerID": 2,
            "listingID": 1
        }
        response = self.client.post('/transaction', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_add_to_wishlist(self):
        data = {
            "userID": 1,
            "listingID": 1
        }
        response = self.client.post('/wishlist', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_wishlist(self):
        response = self.client.get('/wishlist/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
