const userID = getUserId();

function getUserId() {
    const user = localStorage.getItem('user');
    if (user) {
        const userData = JSON.parse(user);
        console.log('User ID:', userData.userID);
        return userData.userID;
    } else {
        console.log('No user data found in localStorage.');
        return null;
    }
}

// Function to fetch and display user listings from the server
async function displayUserListings() {
    const user = JSON.parse(localStorage.getItem('user'));  // Retrieve user from localStorage
    const userID = user ? user.userID : null;

    if (!userID) {
        alert("User not logged in. Please log in to view your listings.");
        return;
    }

    const listingsContainer = document.querySelector('.listings-container');
    listingsContainer.innerHTML = '';  // Clear any previous listings

    try {
        // Fetch listings from the server
        const response = await fetch(`http://127.0.0.1:5000/listings?userID=${userID}`);
        if (!response.ok) {
            throw new Error('Failed to fetch listings');
        }

        const data = await response.json();
        const userListings = data.listings;

        if (userListings.length === 0) {
            listingsContainer.innerHTML = '<p>No listings found. Please add products to sell.</p>';
            return;
        }

        // Loop through each product in the user's listings and display it
        userListings.forEach((listing, index) => {
            const productBlock = document.createElement('div');
            productBlock.classList.add('product-block');
            productBlock.dataset.listingID = listing.listingID;

            // Create the product HTML structure
            productBlock.innerHTML = `
                <div class="border">
                    <div class="product-image">
                        <img src="${listing.images[0] || 'https://via.placeholder.com/150'}" alt="${listing.title}" width="150" height="150">
                    </div>
                    <div class="product-details">
                        <h3 class="product-title">${listing.title}</h3>
                        <p class="product-price">₹ ${listing.selling_price}</p>
                        <p class="product-grade">Grade: ${listing.grade}</p>
                        <p class="product-created">Created on: ${new Date(listing.createdAt).toLocaleDateString()}</p>
                        <button class="delete-btn" data-index="${index}">Delete</button>
                    </div>
                </div>
            `;

            // Append product block to the container
            listingsContainer.appendChild(productBlock);
        });

        // Attach event listeners for the delete button
        const deleteButtons = document.querySelectorAll('.delete-btn');
        deleteButtons.forEach(button => {
            button.addEventListener('click', handleDelete);
        });

    } catch (error) {
        console.error('Error fetching listings:', error);
        listingsContainer.innerHTML = '<p>Error fetching listings. Please try again later.</p>';
    }
}

// Function to handle the deletion of a listing
async function handleDelete(event) {
    const button = event.target;
    const productBlock = button.closest('.product-block');
    const listingID = productBlock.dataset.listingID;

    // Get user data from localStorage
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.userID) {
        alert("User not found. Please log in.");
        return;
    }

    const userID = user.userID;

    // Make DELETE request to the server to remove the listing
    try {
        const response = await fetch(`http://127.0.0.1:5000/listings/${listingID}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userID })  // Include userID in the request body
        });

        if (response.ok) {
            // Remove the product from the DOM
            productBlock.remove();
            alert('Product deleted successfully');
        } else {
            const errorResult = await response.json();
            console.error('Failed to delete product:', errorResult);
            alert('Failed to delete product. Please try again.');
        }

    } catch (error) {
        console.error('Error deleting product:', error);
        alert('An error occurred while deleting the product.');
    }
}

// Load user listings when the page loads
window.onload = function () {
    displayUserListings();
};
