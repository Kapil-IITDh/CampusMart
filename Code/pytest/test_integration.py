from flask_testing import TestCase
from yourapp import app, db  # Replace 'yourapp' with your app's module name

class TestAppIntegration(TestCase):
    def create_app(self):
        # Configure the app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        return app

    def setUp(self):
        db.create_all()  # Create tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Drop tables

    def test_register_and_login_user(self):
        """Test registering and logging in a user with valid and invalid credentials"""
        # Register a new user
        response = self.client.post('/register', json={
            'name': 'Test User',
            'email': 'test@iitdh.ac.in',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'Student',
            'phoneNumber': '1234567890'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'User registered successfully', response.data)

        # Attempt to login with valid credentials
        response = self.client.post('/login', json={
            'email': 'test@iitdh.ac.in',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)

        # Attempt to login with incorrect password
        response = self.client.post('/login', json={
            'email': 'test@iitdh.ac.in',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Invalid credentials', response.data)

    def test_get_all_products(self):
        """Test fetching all products"""
        response = self.client.get('/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'products', response.data)

    def test_add_and_update_product(self):
        """Test adding and updating a product"""
        # Add a product
        response = self.client.post('/product', json={
            'userID': 1,
            'title': 'Test Product',
            'description': 'A product for testing',
            'selling_price': 500,
            'new_item_price': 1000,
            'categoryID': 1,
            'grade': 'A'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Product added successfully', response.data)

        # Update the product
        response = self.client.put('/product/1', json={
            'title': 'Updated Product Title',
            'description': 'Updated product description',
            'selling_price': 450,
            'new_item_price': 900,
            'categoryID': 1,
            'grade': 'A+'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product updated successfully', response.data)

    def test_manage_wishlist(self):
        """Test adding, viewing, and removing items from the wishlist"""
        # Add item to wishlist
        response = self.client.post('/wishlist', json={
            'userID': 1,
            'listingID': 1
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Product added to wishlist successfully', response.data)

        # View wishlist
        response = self.client.get('/wishlist/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'wishlistID', response.data)

        # Remove item from wishlist
        response = self.client.delete('/wishlist/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product removed from wishlist successfully', response.data)

    def test_category_management(self):
        """Test fetching and accessing categories"""
        # Fetch all categories
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Categories', response.data)  # Assuming category data is returned

        # Fetch a specific category by ID
        response = self.client.get('/categories/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'categoryID', response.data)  # Verify category ID field exists in the response

if __name__ == '__main__':
    unittest.main()
