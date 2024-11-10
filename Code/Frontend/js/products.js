async function fetchProducts() {
  try {
      const response = await fetch('http://127.0.0.1:5000/products', {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          }
      });

      if (response.ok) {
          dataset = await response.json();
          console.log('Products dataset:', dataset);
          // Call displayProducts after fetching the data
          displayProducts(dataset);
      } else {
          console.error('Failed to fetch products:', response.statusText);
      }
  } catch (error) {
      console.error('Error:', error);
  }
}

// Function to display products dynamically
function displayProducts(dataset) {
  const productBlockContainer = document.querySelector('.productBlockContainer');

  // Clear existing products to prevent duplication
  productBlockContainer.innerHTML = '';

  // Check if dataset has products before trying to display
  if (dataset && dataset.products && dataset.products.length > 0) {
      // Loop through each product in the products array
      
      dataset.products.forEach(product => {
          const { listingID, title, selling_price, description } = product;
          const imageURLs = JSON.parse(product.imageURLs);
          // Create the URL for the individual product page
          const productPageUrl = `product.html?product_id=${listingID}`;
            // alert(imageURLs[0]);
          // Create product block HTML
          const productBlock = document.createElement('a');
          productBlock.classList.add('productBlock');
          productBlock.href = productPageUrl; // Make the entire card clickable
          productBlock.style.textDecoration = 'none'; // Remove underline
          productBlock.style.color = 'inherit'; // Inherit color
            console.log("ImageUrls: ${imageURLs}",imageURLs);
          productBlock.innerHTML = `
              <div class="border">
                  <div class="productImage">
                  <img src="${ Array.isArray(imageURLs) && imageURLs[0] ? imageURLs[0] : 'https://images.unsplash.com/photo-1484788984921-03950022c9ef?q=80&w=1232&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}" alt="${title}" width="180" height="180">

                     </div>
                  <div class="productTitle">${title}</div>
                  <div class="productPrice">₹ ${selling_price}</div>
              </div>
          `;

          // Append the product block to the container
          productBlockContainer.appendChild(productBlock);
      });
  } else {
      console.log('No products found in the dataset.');
  }
}


// Call the function to fetch and display products on page load
fetchProducts();


// Call the function to display products once the page has loaded
window.onload = displayProducts;