-- Create the database
CREATE DATABASE CampusMart;
USE CampusMart;

-- Create the Users table
CREATE TABLE Users (
    userID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    department VARCHAR(100),
    passwordHash VARCHAR(255) NOT NULL,
    userType ENUM('Student', 'Faculty', 'Staff') NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the Categories table
CREATE TABLE Categories (
    categoryID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- Create the Listings table
CREATE TABLE Listings (
    listingID INT AUTO_INCREMENT PRIMARY KEY,
    userID INT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    categoryID INT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    isActive BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (userID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID) ON DELETE SET NULL
);

-- Create the Transactions table
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

-- Create the Messages table
CREATE TABLE Messages (
    messageID INT AUTO_INCREMENT PRIMARY KEY,
    senderID INT,
    receiverID INT,
    content TEXT NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (senderID) REFERENCES Users(userID) ON DELETE CASCADE,
    FOREIGN KEY (receiverID) REFERENCES Users(userID) ON DELETE CASCADE
);

-- Create the Ratings table
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

-- Create the ListingImages table
CREATE TABLE ListingImages (
    imageID INT AUTO_INCREMENT PRIMARY KEY,
    listingID INT,
    imageURL VARCHAR(255) NOT NULL,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listingID) REFERENCES Listings(listingID) ON DELETE CASCADE
);

-- Insert sample data into Categories table
INSERT INTO Categories (name, description) VALUES
('Books', 'Academic and recreational books'),
('Electronics', 'Phones, laptops, and gadgets'),
('Furniture', 'Desks, chairs, and more'),
('Cycles', 'Bicycles for on-campus commute');

-- Insert sample data into Users table
INSERT INTO Users (name, email, department, passwordHash, userType) VALUES
(
    ------
);

-- Insert a new listing into the Listings table
INSERT INTO Listings (userID, title, description, price, categoryID)
VALUES (1, 'Physics Textbook', 'Advanced Physics book in good condition', 500, 1);

-- Assuming the listingID for the above insertion is 1 (auto-incremented ID)
-- Insert multiple images into the ListingImages table for the same listing
INSERT INTO ListingImages (listingID, imageURL) VALUES (1, 'Link1');
INSERT INTO ListingImages (listingID, imageURL) VALUES (1, 'Link2');
INSERT INTO ListingImages (listingID, imageURL) VALUES (1, 'Link3');


-- Query for searching listings
SELECT * FROM Listings WHERE title LIKE '%Bycycle%' AND isActive = TRUE;

-- Query for viewing transaction history
SELECT * FROM Transactions WHERE buyerID = 1 OR sellerID = 1;

-- Create triggers
-- Trigger to mark transaction as completed after rating
CREATE TRIGGER complete_transaction_after_rating
AFTER INSERT ON Ratings
FOR EACH ROW
BEGIN
   UPDATE Transactions
   SET status = 'Completed'
   WHERE transactionID = NEW.transactionID;
END;

-- Trigger to make listing inactive after transaction is completed
CREATE TRIGGER set_listing_inactive_after_transaction
AFTER UPDATE ON Transactions
FOR EACH ROW
BEGIN
   IF NEW.status = 'Completed' THEN
      UPDATE Listings
      SET isActive = FALSE
      WHERE listingID = NEW.listingID;
   END IF;
END;

-- Indexing for optimization
CREATE INDEX idx_userID ON Listings(userID);
CREATE INDEX idx_buyerID ON Transactions(buyerID);
CREATE INDEX idx_sellerID ON Transactions(sellerID);
