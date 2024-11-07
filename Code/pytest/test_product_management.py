import unittest
from yourapp import app

class TestProductManagement(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        # Assume a user has already been created for product creation
        self.client.post('/register', json={
            'name': 'John Doe',
            'email': 'john@iitdh.ac.in',
            'department': 'CSE',
            'password': 'password123',
            'userType': 'Student',
            'phoneNumber': '1234567890'
        })

    def test_add_product_with_valid_data(self):
        """Test adding a product with valid data"""
        response = self.client.post('/product', json={
            'userID': 1,
            'title': 'Laptop',
            'description': 'A high-end laptop',
            'selling_price': 1000,
            'new_item_price': 1200,
            'categoryID': 1,
            'grade': 'A'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Product added successfully', response.data)

    def test_add_product_with_missing_fields(self):
        """Test adding a product with missing fields"""
        response = self.client.post('/product', json={
            'userID': 1,
            'title': 'Laptop'
            # Missing description, price, categoryID, etc.
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing', response.data)

    def test_update_existing_product(self):
        """Test updating an existing product"""
        # First, add a product
        self.client.post('/product', json={
            'userID': 1,
            'title': 'Laptop',
            'description': 'A high-end laptop',
            'selling_price': 1000,
            'new_item_price': 1200,
            'categoryID': 1,
            'grade': 'A'
        })

        # Update the product
        response = self.client.put('/product/1', json={
            'title': 'Updated Laptop',
            'description': 'Updated description',
            'selling_price': 950,
            'new_item_price': 1100,
            'categoryID': 1,
            'grade': 'A+'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product updated successfully', response.data)

    def test_delete_product(self):
        """Test deleting a product"""
        # Add a product to delete
        self.client.post('/product', json={
            'userID': 1,
            'title': 'Laptop',
            'description': 'A high-end laptop',
            'selling_price': 1000,
            'new_item_price': 1200,
            'categoryID': 1,
            'grade': 'A'
        })

        # Delete the product
        response = self.client.delete('/product/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product deleted successfully', response.data)

    def test_get_nonexistent_product(self):
        """Test fetching a product that doesn't exist"""
        response = self.client.get('/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Product not found', response.data)

if __name__ == '__main__':
    unittest.main()
