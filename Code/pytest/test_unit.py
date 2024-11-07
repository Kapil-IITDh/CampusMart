import unittest
from unittest.mock import patch, MagicMock
from yourapp import app, get_db_connection  # Replace 'yourapp' with your Flask app's module name

class TestAppUnit(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_home_page(self):
        """Test the home page route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello, welcome to CampusMart API!", response.data)

    @patch('yourapp.mysql.connector.connect')
    def test_get_db_connection_successful(self, mock_connect):
        """Test successful database connection"""
        mock_connect.return_value = MagicMock()
        conn = get_db_connection()
        self.assertIsNotNone(conn)

    @patch('yourapp.mysql.connector.connect')
    def test_get_db_connection_failure(self, mock_connect):
        """Test database connection failure"""
        mock_connect.side_effect = Exception("Connection error")
        conn = get_db_connection()
        self.assertIsNone(conn)

    def test_invalid_user_type_in_register(self):
        """Test /register route with invalid user type"""
        response = self.client.post('/register', json={
            'name': 'Test User',
            'email': 'test@iitdh.ac.in',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'InvalidType',
            'phoneNumber': '1234567890'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid userType', response.data)

    def test_register_with_missing_fields(self):
        """Test /register route with missing fields"""
        response = self.client.post('/register', json={
            'name': 'Test User',
            'email': 'test@iitdh.ac.in',
            'userType': 'Student'
            # Missing other required fields
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing', response.data)  # Assuming missing field triggers error

    def test_login_with_missing_email(self):
        """Test /login route with missing email field"""
        response = self.client.post('/login', json={
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'email is required', response.data)  # Assuming missing field triggers error

    def test_add_product_with_incomplete_data(self):
        """Test /product route with incomplete data"""
        response = self.client.post('/product', json={
            'title': 'Test Product',
            'selling_price': 500,
            # Missing other required fields like userID, description, categoryID
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing', response.data)

if __name__ == '__main__':
    unittest.main()
