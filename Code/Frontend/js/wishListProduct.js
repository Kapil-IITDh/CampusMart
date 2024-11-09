// Sample test dataset to simulate real product data
var wishListItems = {
    products: [
        {
            listingID: 1,
            title: "Laptop",
            selling_price: 50000,
            description: "A high-performance laptop with 16GB RAM and 512GB SSD.",
            imageURLs: [
                'https://images.unsplash.com/photo-1542751110-70e56cd58e6e'
            ]
        },
    ]
};
localStorage.setItem('wishListItems',JSON.stringify(wishListItems));
console.log("hello duniya");



// Function to display products dynamically
function displayProducts(dataset) {
    const productBlockContainer = document.querySelector('.productBlockContainer');

    // Clear existing products to prevent duplication
    productBlockContainer.innerHTML = '';

    // Check if dataset has products before trying to display
    if (dataset && dataset.products && dataset.products.length > 0) {
        // Loop through each product in the products array
        dataset.products.forEach((product, index) => {
            const imageURLs = JSON.parse(product.imageURLs);
            const { listingID, title, selling_price } = product;
            console.log(`Image URLs:`, imageURLs);
            // Create the URL for the individual product page
            const productPageUrl = `product.html?product_id=${listingID}`;

            // Create product block HTML
            const productBlock = document.createElement('div');
            productBlock.classList.add('productBlock');
            productBlock.dataset.listingID = listingID;  // Add dataset attribute to identify the product

            productBlock.innerHTML = `
                <div class="border">
                    <div class="productImage">
                        <img src="${imageURLs[0] ? imageURLs[0] : 'https://images.unsplash.com/photo-1484788984921-03950022c9ef?q=80&w=1232&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}" alt="${title}" width="180" height="180">
                    </div>
                    <div class="productDetails">
                        <div class="productTitle">${title}</div>
                        <div class="productPrice">₹ ${selling_price}</div>
                        <a href="${productPageUrl}" class="viewProductButton">
                            <button type="button" class="viewProductButton">View Product</button>
                        </a>
                        <button type="button" class="deleteButton" data-index="${index}">Delete</button>
                    </div>
                </div>
            `;

            // Append the product block to the container
            productBlockContainer.appendChild(productBlock);
        });

        // Add event listeners to the delete buttons
        const deleteButtons = document.querySelectorAll('.deleteButton');
        deleteButtons.forEach(button => {
            button.addEventListener('click', handleDelete);
        });
    } else {
        console.log('No products found in the dataset.');
    }
}

// Delete handler function
async function handleDelete(event) {
    const button = event.target;  // The clicked delete button
    const productBlock = button.closest('.productBlock');  // Find the parent product block
    const listingID = productBlock.dataset.listingID;  // Get the listing ID from the data attribute
    const user = JSON.parse(localStorage.getItem('user'));  // Get user data from localStorage

    if (!user || !user.userID) {
        alert("User not found. Please log in.");
        return;
    }

    const userID = user.userID;

    // Find the product in the dataset based on listingID
    const productIndex = wishListItems.products.findIndex(product => product.listingID === parseInt(listingID));

    if (productIndex !== -1) {
        try {
            // Make a DELETE request to the server with userID included in the body
            const response = await fetch(`http://127.0.0.1:5000/wishlist/${listingID}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ userID })  // Include userID in the request body
            });

            if (response.ok) {
                // Remove the product from the dataset
                wishListItems.products.splice(productIndex, 1);

                // Remove the product block from the DOM
                productBlock.remove();

                console.log(`Product with ID ${listingID} deleted from the wishlist.`);
                alert('Product removed from wishlist successfully');
            } else {
                const errorResult = await response.json();
                console.error('Failed to delete product from wishlist:', errorResult);
                alert('Failed to delete product from wishlist. Please try again.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while deleting the product from the wishlist.');
        }
    }
}

// Test the displayProducts function by passing the test dataset



// Function to fetch the wishlist from the server
async function fetchWishlist(userId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/wishlist/${userId}`);
        if (response.ok) {
            const data = await response.json();
            console.log('Wishlist data fetched:', data);

            // Update the `wishListItems` and save to localStorage
            wishListItems = data;
            localStorage.setItem('wishListItems', JSON.stringify(wishListItems));

            // Display the products in the wishlist
            displayProducts(wishListItems);
        } else {
            const errorData = await response.json();
            console.error('Failed to fetch wishlist:', errorData.error);
        }
    } catch (error) {
        console.error('Error while fetching wishlist:', error);
    }
}



window.onload = function() {
    const user = JSON.parse(localStorage.getItem('user'));  // Ensure the user data is stored during login
    const userId = user ? user.userID : null;
    // alert(userId);
    if (userId) {
        fetchWishlist(userId);
    } else {
        console.log('User is not logged in. Please log in to view the wishlist.');
    }
};