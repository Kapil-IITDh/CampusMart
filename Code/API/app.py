from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '``````'
app.config['MYSQL_DB'] = 'campusmart'

mysql = MySQL(app)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Function to save images and return their URLs
def save_images(files):
    image_urls = []
    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_urls.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return image_urls

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)",
                   (data['username'], data['password'], data['email']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'User registered successfully'}), 201

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s",
                   (data['username'], data['password']))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Add a new product
@app.route('/product', methods=['POST'])
def add_product():
    data = request.form
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Products (category, product_name, price, description, rating, condition, purchase_rate, selling_rate, used_for_months) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (data['category'], data['product_name'], data['price'], data['description'], data['rating'], data['condition'], data['purchase_rate'], data['selling_rate'], data['used_for_months']))
    product_id = cursor.lastrowid
    
    files = request.files.getlist('images')
    image_urls = save_images(files)
    for url in image_urls:
        cursor.execute("INSERT INTO ProductImages (product_id, image_url) VALUES (%s, %s)", (product_id, url))
    
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product added successfully'}), 201

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    cursor.close()
    return jsonify({'products': products}), 200

# Get product details by id
@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    cursor.execute("SELECT image_url FROM ProductImages WHERE product_id = %s", (product_id,))
    images = cursor.fetchall()
    cursor.close()
    return jsonify({'product': product, 'images': images}), 200

# Message between buyer and seller
@app.route('/message', methods=['POST'])
def send_message():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO Messages (sender_id, receiver_id, message, timestamp) VALUES (%s, %s, %s, NOW())",
                   (data['sender_id'], data['receiver_id'], data['message']))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Message sent successfully'}), 201

# Get all messages between two users
@app.route('/messages', methods=['GET'])
def get_messages():
    sender_id = request.args.get('sender_id')
    receiver_id = request.args.get('receiver_id')
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s) ORDER BY timestamp",
                   (sender_id, receiver_id, receiver_id, sender_id))
    messages = cursor.fetchall()
    cursor.close()
    return jsonify({'messages': messages}), 200

# API to get all unique contacts (users) a specific user has chatted with
@app.route('/contacts/<int:user_id>', methods=['GET'])
def get_contacts(user_id):
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT DISTINCT CASE WHEN sender_id = %s THEN receiver_id ELSE sender_id END AS contact_id
        FROM Messages
        WHERE sender_id = %s OR receiver_id = %s
    """, (user_id, user_id, user_id))
    contacts = cursor.fetchall()
    cursor.close()
    return jsonify({'contacts': contacts}), 200

# Update product details
@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE Products SET category=%s, product_name=%s, price=%s, description=%s, rating=%s, condition=%s, purchase_rate=%s, selling_rate=%s, used_for_months=%s WHERE id=%s",
                   (data['category'], data['product_name'], data['price'], data['description'], data['rating'], data['condition'], data['purchase_rate'], data['selling_rate'], data['used_for_months'], product_id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product updated successfully'}), 200

# Delete a product
@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM Products WHERE id = %s", (product_id,))
    cursor.execute("DELETE FROM ProductImages WHERE product_id = %s", (product_id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Product deleted successfully'}), 200

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
