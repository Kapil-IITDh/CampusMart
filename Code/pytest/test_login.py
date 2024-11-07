import unittest
from yourapp import app

class TestUserLogin(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Register a test user for login tests
        self.client.post('/register', json={
            'name': 'John Doe',
            'email': 'john@iitdh.ac.in',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'Student',
            'phoneNumber': '1234567890'
        })

    def test_login_with_correct_credentials(self):
        """Test logging in with correct credentials"""
        response = self.client.post('/login', json={
            'email': 'john@iitdh.ac.in',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

    def test_login_with_incorrect_password(self):
        """Test logging in with an incorrect password"""
        response = self.client.post('/login', json={
            'email': 'john@iitdh.ac.in',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)

    def test_login_with_nonexistent_email(self):
        """Test logging in with a non-existent email"""
        response = self.client.post('/login', json={
            'email': 'nonexistent@iitdh.ac.in',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)

    def test_login_with_missing_password(self):
        """Test logging in with a missing password"""
        response = self.client.post('/login', json={
            'email': 'john@iitdh.ac.in'
            # Password missing
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'password is required', response.data)

    def test_login_with_empty_request_body(self):
        """Test logging in with an empty request body"""
        response = self.client.post('/login', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing email and password', response.data)

if __name__ == '__main__':
    unittest.main()
