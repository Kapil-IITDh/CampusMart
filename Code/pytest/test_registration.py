import unittest
from app import app

class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_register_with_valid_data(self):
        """Test registering with valid user data"""
        response = self.client.post('/register', json={
            'name': 'John Doe',
            'email': 'john@iitdh.ac.in',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'Student',
            'phoneNumber': '1234567890'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

    def test_register_with_invalid_user_type(self):
        """Test registering with an invalid user type"""
        response = self.client.post('/register', json={
            'name': 'John Doe',
            'email': 'john@iitdh.ac.in',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'InvalidType',
            'phoneNumber': '1234567890'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid userType', response.data)

    def test_register_with_missing_fields(self):
        """Test registration with missing required fields"""
        response = self.client.post('/register', json={
            'name': 'John Doe',
            'email': 'john@iitdh.ac.in',
            # Missing department, password, userType, and phoneNumber
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing', response.data)

    def test_register_with_invalid_email_format(self):
        """Test registering with an invalid email format"""
        response = self.client.post('/register', json={
            'name': 'John Doe',
            'email': 'johnexample.com',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'Student',
            'phoneNumber': '1234567890'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid email', response.data)

    def test_register_with_duplicate_email(self):
        """Test registering with an email that already exists"""
        # First registration
        self.client.post('/register', json={
            'name': 'John Doe',
            'email': 'john@iitdh.ac.in',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'Student',
            'phoneNumber': '1234567890'
        })

        # Attempt duplicate registration
        response = self.client.post('/register', json={
            'name': 'Jane Doe',
            'email': 'john@iitdh.ac.in',
            'department': 'ECE',
            'password': 'newpassword123',
            'userType': 'Faculty',
            'phoneNumber': '0987654321'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'email already exists', response.data)

if __name__ == '__main__':
    unittest.main()
