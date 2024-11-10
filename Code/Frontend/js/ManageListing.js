// Simulate user data in localStorage for testing purposes
if (!localStorage.getItem('user')) {
    // Simulating user login
    localStorage.setItem('user', JSON.stringify({ userID: "123" }));
}

const user = JSON.parse(localStorage.getItem('user'));
if (!user) {
    alert("Please log in to manage your listings.");
    window.location.href = "./signin.html";  // Redirect to login page if not logged in
}

// Function to fetch and display user listings from the server
async function displayUserListings() {
    const userId = user.userID;  // Get user ID from localStorage
    const listingsContainer = document.querySelector('.listings-container');
    listingsContainer.innerHTML = '';  // Clear any previous listings

    try {
        // Fetch listings from the server
        const response = await fetch(`http://127.0.0.1:5000/listings/${userId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch listings');
        }
        const userListings = await response.json();

        if (userListings.length === 0) {
            listingsContainer.innerHTML = '<p>No listings found. Please add products to sell.</p>';
            return;
        }

        // Loop through each product in the user's listings and display it
        userListings.forEach((listing, index) => {
            const productBlock = document.createElement('div');
            productBlock.classList.add('product-block');
            productBlock.dataset.listingID = listing.listingID;

            // Create the product HTML structure (without description and edit button)
            productBlock.innerHTML = `
                <div class="border">
                    <div class="product-image">
                        <img src="${listing.imageURLs[0] || 'https://via.placeholder.com/150'}" alt="${listing.title}" width="150" height="150">
                    </div>
                    <div class="product-details">
                        <h3 class="product-title">${listing.title}</h3>
                        <p class="product-price">₹ ${listing.selling_price}</p>
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
