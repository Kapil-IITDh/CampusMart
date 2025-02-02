USE parsec;

CREATE TABLE Users (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(100),
    passwordHash VARCHAR(255) NOT NULL,
    userType ENUM('Student', 'Faculty', 'Staff') NOT NULL,
    phoneNumber VARCHAR(15),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Categories (
    categoryID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE Listings (
    listingID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    selling_price DECIMAL(10, 2) NOT NULL,
    new_item_price DECIMAL(10, 2),
    categoryID INT,
    grade INT CHECK(grade >= 1 AND grade <= 5),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    isActive BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID) ON DELETE SET NULL
);

CREATE TABLE Transactions (
    transactionID INT AUTO_INCREMENT PRIMARY KEY,
    buyerID INT,
    sellerID INT,
    listingID INT,
    amount DECIMAL(10, 2) NOT NULL,
    status ENUM('Pending', 'Completed', 'Disputed') DEFAULT 'Pending',
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (buyerID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (sellerID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (listingID) REFERENCES Listings(listingID) ON DELETE CASCADE
);

CREATE TABLE Messages (
    messageID INT AUTO_INCREMENT PRIMARY KEY,
    senderID INT,
    receiverID INT,
    content TEXT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (senderID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (receiverID) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE Ratings (
    ratingID INT AUTO_INCREMENT PRIMARY KEY,
    transactionID INT,
    raterID INT,
    rateeID INT,
    rating TINYINT CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transactionID) REFERENCES Transactions(transactionID) ON DELETE CASCADE,
    FOREIGN KEY (raterID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (rateeID) REFERENCES Users(userID) ON DELETE CASCADE
);

CREATE TABLE ListingImages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    listingID INT,
    imgURL TEXT,
    FOREIGN KEY (listingID) REFERENCES Listings(listingID) ON DELETE CASCADE
);

CREATE INDEX idx_userID ON Listings(userID);
CREATE INDEX idx_buyerID ON Transactions(buyerID);
CREATE INDEX idx_sellerID ON Transactions(sellerID);

INSERT INTO Users (name, email, department, passwordHash, userType, phoneNumber) VALUES
('Kapil', 'kapil@gmail.com', 'Computer Science', 'hashed_password_kapil', 'Student', '1234567890'),
('Mridul', 'mridul@gmail.com', 'Electrical Engineering', 'hashed_password_mridul', 'Student', '0987654321'),
('Manish', 'manish@gmail.com', 'Mechanical Engineering', 'hashed_password_manish', 'Student', '1122334455');

INSERT INTO Categories (name, description) VALUES
('Electronics', 'Devices such as smartphones, laptops, and other electronic gadgets.'),
('Books', 'Printed or digital publications for reading and education.'),
('Clothing', 'Wearable items including shirts, pants, and accessories.'),
('Sports', 'Equipment and apparel related to various sports activities.'),
('Furniture', 'Items used to furnish living spaces, like chairs and tables.'),
('Stationery', 'Writing materials and office supplies.'),
('Gaming', 'Video games and related accessories.'),
('Appliances', 'Home appliances such as refrigerators, microwaves, and washing machines.');
