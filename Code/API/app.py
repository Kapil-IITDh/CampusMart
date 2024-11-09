from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app,resources={r'*':{'origins':'*'}}) #allow all origin



# Configuration for uploading files
app.config['UPLOAD_FOLDER'] = 'uploads'  # Define your upload folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create the folder if it doesn't exist

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Kapil@8333",
            database="CampusMart"
        )
        print("Connection is successful")
    except mysql.connector.Error as err:
        print(f"Database connection error occurred: {err}")
        return None
    return conn

@app.route('/')
def home_page():
    return jsonify(message="Hello, welcome to CampusMart API!")

# User-related endpoints
# @app.route("/users", methods=['GET'])
# def get_all_users():
#     conn = get_db_connection()
#     if conn is None:
#         return jsonify({'error': 'Database connection failed'}), 500

#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT userID, name, email, department, userType, phoneNumber, createdAt, updatedAt FROM Users")
#     users = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return jsonify(users)

@app.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT userID, name, email, department, userType, phoneNumber, createdAt, updatedAt 
        FROM Users 
        WHERE userID = %s
    """, (user_id,))
    
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    # Validate that userType is one of the ENUM values
    if data['userType'] not in ['Student', 'Faculty', 'Staff']:
        return jsonify({'error': 'Invalid userType. Must be "Student", "Faculty", or "Staff".'}), 400

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            INSERT INTO Users (name, email, department, passwordHash, userType, phoneNumber)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['name'], data['email'], data['department'], data['password'], data['userType'], data['phoneNumber']))
        conn.commit()

        # Retrieve the newly created user data without sensitive fields
        cursor.execute("""
            SELECT userID, name, email, department, userType, phoneNumber
            FROM Users
            WHERE email = %s
        """, (data['email'],))
        new_user = cursor.fetchone()

        cursor.close()
        conn.close()

        if new_user:
            return jsonify({'message': 'User registered successfully', 'user': new_user}), 201
        else:
            return jsonify({'error': 'User registration failed'}), 400

    except Exception as e:
        # Handle potential errors, such as duplicate email
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 400



from flask import request, jsonify
import hashlib

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT userID, name, email, phoneNumber, department, userType FROM Users WHERE email = %s AND passwordHash = %s",
                   (data['email'], data['password']))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


# Categories endpoints
@app.route('/categories', methods=['GET'])
def get_all_categories():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(categories)





@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Categories WHERE categoryID = %s", (category_id,))
    category = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if category:
        return jsonify(category), 200
    else:
        return jsonify({'error': 'Category not found'}), 404

# Listings endpoints
import json

# Listings endpoints
@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            l.*, 
            COALESCE(JSON_ARRAYAGG(li.imgURL), JSON_ARRAY()) AS imageURLs
        FROM Listings l
        LEFT JOIN ListingImages li ON l.listingID = li.listingID
        GROUP BY l.listingID
    """)
    
    products = cursor.fetchall()
    cursor.close()
    conn.close()

    if products:
        return jsonify({'products': products}), 200
    else:
        return jsonify({'error': 'No products found'}), 404


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            l.*, 
            COALESCE(JSON_ARRAYAGG(li.imgURL), JSON_ARRAY()) AS imageURLs
        FROM Listings l
        LEFT JOIN ListingImages li ON l.listingID = li.listingID
        WHERE l.listingID = %s
        GROUP BY l.listingID
    """, (product_id,))
    
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if product:
        return jsonify(product), 200
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/product', methods=['POST'])
def add_product():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert into Listings table
    cursor.execute("INSERT INTO Listings (userID, title, description, selling_price, new_item_price, categoryID, grade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (data['userID'], data['title'], data['description'], data['selling_price'], data['new_item_price'], data['categoryID'], data['grade']))
    listing_id = cursor.lastrowid

    # Handle images
    if 'images' in data:
        for img_url in data['images']:
            cursor.execute("INSERT INTO ListingImages (listingID, imgURL) VALUES (%s, %s)", (listing_id, img_url))
    
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product added successfully'}), 201

@app.route('/product/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("UPDATE Listings SET title=%s, description=%s, selling_price=%s, new_item_price=%s, categoryID=%s, grade=%s WHERE listingID=%s",
                   (data['title'], data['description'], data['selling_price'], data['new_item_price'], data['categoryID'], data['grade'], product_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product updated successfully'}), 200

@app.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Listings WHERE listingID = %s", (product_id,))
    cursor.execute("DELETE FROM ListingImages WHERE listingID = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product deleted successfully'}), 200

# ListingImages endpoints
@app.route('/listing_images', methods=['GET'])
def get_listing_images():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ListingImages")
    images = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(images)

@app.route('/listing_images/<int:listing_id>', methods=['GET'])
def get_listing_images_by_listing(listing_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ListingImages WHERE listingID = %s", (listing_id,))
    images = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(images)

# Messages endpoints
@app.route('/messages/<int:user_id>', methods=['GET'])
def get_all_messages(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            m.messageID,
            m.senderID,
            sender.name AS senderName,
            m.receiverID,
            receiver.name AS receiverName,
            m.content,
            m.createdAt
        FROM Messages m
        JOIN Users sender ON m.senderID = sender.userID
        JOIN Users receiver ON m.receiverID = receiver.userID
        WHERE m.senderID = %s OR m.receiverID = %s
        ORDER BY m.createdAt
    """, (user_id, user_id))
    
    messages = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(messages), 200



@app.route('/message', methods=['POST'])
def send_message():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    # Corrected SQL statement: removed the semicolon within the SQL string
    cursor.execute(
        "INSERT INTO Messages (senderID, receiverID, content, createdAt) VALUES (%s, %s, %s, NOW())",
        (data['sender_id'], data['receiver_id'], data['message'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Message sent successfully'}), 201


@app.route('/users/<int:user_id>/chats', methods=['GET'])
def get_chatted_users(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT DISTINCT
            CASE
                WHEN m.senderID = %s THEN m.receiverID
                ELSE m.senderID
            END AS user_id,
            CASE
                WHEN m.senderID = %s THEN u2.name
                ELSE u1.name
            END AS user_name
        FROM Messages m
        JOIN Users u1 ON m.senderID = u1.userID
        JOIN Users u2 ON m.receiverID = u2.userID
        WHERE m.senderID = %s OR m.receiverID = %s
    """, (user_id, user_id, user_id, user_id))

    users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(users), 200





# Ratings endpoints
@app.route('/ratings', methods=['GET'])
def get_all_ratings():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Ratings")
    ratings = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(ratings)

@app.route('/rating', methods=['POST'])
def add_rating():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("INSERT INTO Ratings (listingID, userID, ratingValue) VALUES (%s, %s, %s)",
                   (data['listingID'], data['userID'], data['ratingValue']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Rating added successfully'}), 201

# Transactions endpoints
@app.route('/transactions', methods=['GET'])
def get_all_transactions():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Transactions")
    transactions = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(transactions)

@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("INSERT INTO Transactions (buyerID, sellerID, listingID, transactionDate) VALUES (%s, %s, %s, NOW())",
                   (data['buyerID'], data['sellerID'], data['listingID']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Transaction added successfully'}), 201


@app.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)  # Ensure dictionary output

    # Query to check if the listing is active
    cursor.execute("SELECT isActive FROM Listings WHERE listingID = %s", (data['listingID'],))
    listing = cursor.fetchone()

    if listing is None or not listing['isActive']:  # This now correctly checks the value
        cursor.close()
        conn.close()
        return jsonify({'error': 'Listing is inactive or does not exist'}), 400  # 400 for bad request

    # Insert the listing into the Wishlists table
    cursor.execute("INSERT INTO Wishlists (userID, listingID) VALUES (%s, %s)",
                   (data['userID'], data['listingID']))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Product added to wishlist successfully'}), 201


@app.route('/wishlist/<int:wishlist_id>', methods=['DELETE'])
def remove_from_wishlist(wishlist_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    cursor.execute("DELETE FROM Wishlists WHERE wishlistID = %s", (wishlist_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product removed from wishlist successfully'}), 200


@app.route('/wishlist/<int:user_id>', methods=['GET'])
def get_wishlist(user_id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            w.listingID,
            l.title,
            l.selling_price,
            l.description,
            IFNULL(JSON_ARRAYAGG(li.imgURL), JSON_ARRAY()) AS imageURLs
        FROM Wishlists w
        JOIN Listings l ON w.listingID = l.listingID
        LEFT JOIN ListingImages li ON l.listingID = li.listingID
        WHERE w.userID = %s
        GROUP BY w.listingID
    """, (user_id,))

    wishlist = cursor.fetchall()
    cursor.close()
    conn.close()

    if wishlist:
        return jsonify({'products': wishlist}), 200
    else:
        return jsonify({'error': 'No wishlist items found'}), 404



# Start the Flask app
if __name__ == '__main__':
    app.run(port=5000,debug=True)

