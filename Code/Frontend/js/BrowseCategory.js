// Global variable to store the products data
let productsData = [];

// Function to fetch products data from the API and store it in productsData
async function fetchProducts() {
    try {
        const response = await fetch('http://127.0.0.1:5000/products');
        if (response.ok) {
            const data = await response.json();
            productsData = data.products; // Store the response data in productsData
            console.log('Products data fetched successfully:', productsData);
            renderSidebar(); // Render the sidebar with category options
            displayProducts('All Categories'); // Display all products by default
        } else {
            console.error('Failed to fetch products data:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching products data:', error);
    }
}

// Function to create product cards
function createProductCard(product) {
    const imageUrl = JSON.parse(product.imageURLs)[0] || 'https://via.placeholder.com/150'; // Parse imageURLs and use the first image
    return `
   <a href="http://127.0.0.1:5502/Code/Frontend/product.html?product_id=${product.listingID}" 
   style="text-decoration: none; color: inherit;">
    <div class="product-card">
        <img src="${imageUrl}" alt="${product.title}">
        <div class="product-name">${product.title}</div>
        <div class="product-price">Price: ₹${product.selling_price}</div>
        <div class="product-description">${product.description}</div>
    </div>
</a>
    `;
}

// Function to display products for a selected category or all categories
function displayProducts(categoryID) {
    const productContainer = document.getElementById('product-container');
    let productsToDisplay = [];

    if (categoryID === 'All Categories') {
        productsToDisplay = productsData; // Display all products
    } else {
        // Display products that match the selected category ID
        productsToDisplay = productsData.filter(product => product.categoryID === parseInt(categoryID));
    }

    productContainer.innerHTML = productsToDisplay.length > 0
        ? productsToDisplay.map(createProductCard).join('')
        : '<p>No products found for this category.</p>';
}

// Function to render category checkboxes in the sidebar
function renderSidebar() {
    const sidebar = document.getElementById('category-sidebar');

    // Get unique categories with their IDs and names
    const uniqueCategories = [...new Map(productsData.map(product => [product.categoryID, product.categoryName])).entries()];

    // Add "All Categories" option at the top
    sidebar.innerHTML = `
        <div class="category-checkbox">
            <input type="radio" name="category" value="All Categories" id="AllCategories" onclick="displayProducts('All Categories')" checked>
            <label for="AllCategories">All Categories</label>
        </div>
    ` + uniqueCategories.map(([categoryID, categoryName]) => `
        <div class="category-checkbox">
            <input type="radio" name="category" value="${categoryID}" id="category-${categoryID}" onclick="displayProducts('${categoryID}')">
            <label for="category-${categoryID}">${categoryName}</label>
        </div>
    `).join('');
}

// Call the function to fetch products when the page loads
document.addEventListener('DOMContentLoaded', fetchProducts);
