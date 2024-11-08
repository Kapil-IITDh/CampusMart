// Sample test dataset to simulate real product data
const testDataset = {
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
        {
            listingID: 2,
            title: "Bicycle",
            selling_price: 15000,
            description: "Mountain bicycle with a sturdy frame and suspension.",
            imageURLs: [
                'https://images.unsplash.com/photo-1519887386798-e0b5d70ff4ff'
            ]
        },
        {
            listingID: 3,
            title: "Shoe Rack",
            selling_price: 2500,
            description: "Wooden shoe rack with 5 shelves.",
            imageURLs: [
                'https://images.unsplash.com/photo-1590712617227-8a0b6a6f1d07'
            ]
        },
        {
            listingID: 4,
            title: "Smartphone",
            selling_price: 30000,
            description: "Latest smartphone with a powerful camera and battery life.",
            imageURLs: [
                'https://images.unsplash.com/photo-1593630355331-25f27ab0c8c1'
            ]
        }
    ]
};

// Function to display products dynamically
function displayProducts(dataset) {
    const productBlockContainer = document.querySelector('.productBlockContainer');

    // Clear existing products to prevent duplication
    productBlockContainer.innerHTML = '';

    // Check if dataset has products before trying to display
    if (dataset && dataset.products && dataset.products.length > 0) {
        // Loop through each product in the products array
        dataset.products.forEach((product, index) => {
            const { listingID, title, selling_price, imageURLs } = product;

            // Create the URL for the individual product page
            const productPageUrl = `product.html?product_id=${listingID}`;

            // Create product block HTML
            const productBlock = document.createElement('div');
            productBlock.classList.add('productBlock');
            productBlock.dataset.listingID = listingID;  // Add dataset attribute to identify the product

            productBlock.innerHTML = `
                <div class="border">
                    <div class="productImage">
                        <img src="${imageURLs[0]=='null' ? imageURLs[0] : 'https://images.unsplash.com/photo-1484788984921-03950022c9ef?q=80&w=1232&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}" alt="${title}" width="180" height="180">
                    </div>
                    <div class="productDetails">
                        <div class="productTitle">${title}</div>
                        <div class="productPrice">₹ ${selling_price}</div>
                        <a href="${productPageUrl}" class="viewProductButton">
                            <button type="button" class="viewProductButton">View Product</button>
                        </a>
                        <a href="./message.html">
                            <button type="button" class="makeAnOfferButton">Make an offer</button>
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
function handleDelete(event) {
    const button = event.target;  // The clicked delete button
    const productBlock = button.closest('.productBlock');  // Find the parent product block
    const listingID = productBlock.dataset.listingID;  // Get the listing ID from the data attribute

    // Find the product in the dataset based on listingID
    const productIndex = testDataset.products.findIndex(product => product.listingID === parseInt(listingID));

    if (productIndex !== -1) {
        // Remove the product from the dataset
        testDataset.products.splice(productIndex, 1);

        // Remove the product block from the DOM
        productBlock.remove();

        console.log(`Product with ID ${listingID} deleted.`);
    }
}

// Test the displayProducts function by passing the test dataset
window.onload = function() {
    displayProducts(testDataset);
};
