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
          const { listingID, title, selling_price, description, imageURLs } = product;

          // Create the URL for the individual product page
          const productPageUrl = `product.html?product_id=${listingID}`;

          // Create product block HTML
          const productBlock = document.createElement('a');
          productBlock.classList.add('productBlock');
          productBlock.href = productPageUrl; // Make the entire card clickable
          productBlock.style.textDecoration = 'none'; // Remove underline
          productBlock.style.color = 'inherit'; // Inherit color

          productBlock.innerHTML = `
              <div class="border">
                  <div class="productImage">
                  <img src="${ imageURLs[0]=='null' ? imageURLs[0] : 'https://images.unsplash.com/photo-1484788984921-03950022c9ef?q=80&w=1232&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'}" alt="${title}" width="180" height="180">

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

// After connecting to the backend

// // Function to fetch product data from the backend
// function fetchProductData() {
//     // Use fetch to get data from the backend
//     fetch('/api/products')  // Replace this with your actual API endpoint
//         .then(response => {
//             // Check if the response is OK (status 200-299)
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json();  // Parse JSON data
//         })
//         .then(data => {
//             // Call the function to display products
//             displayProducts(data);
//         })
//         .catch(error => {
//             console.error('There was a problem with the fetch operation:', error);
//         });
// }

// // Function to display products dynamically
// function displayProducts(dataset) {
//     const productBlockContainer = document.querySelector('.productBlockContainer');
    
//     // Check if data is received correctly
//     if (!dataset || !dataset.products) {
//         console.error('No product data available');
//         return;
//     }

//     // Loop through each product in the products array
//     dataset.products.forEach(product => {
//         const { listingID, title, selling_price, description } = product;

//         // Create the URL for the individual product page
//         const productPageUrl = `/product/${listingID}`;

//         // Create product block HTML
//         const productBlock = document.createElement('div');
//         productBlock.classList.add('productBlock');
        
//         // Wrap the entire product block in a link tag that points to the product's page
//         productBlock.innerHTML = `
//             <a href="${productPageUrl}" class="productLink">
//                 <div class="border">
//                     <a class="productImage">
//                         <img src="path/to/default-image.jpg" alt="${title}" width="180" height="180">
//                     </a>
//                     <div class="productTitle">${title}</div>
//                     <div class="productPrice">₹ ${selling_price}</div>
//                 </div>
//             </a>
//         `;
  
//         // Append the product block to the container
//         productBlockContainer.appendChild(productBlock);
//     });
// }

// // Call the fetch function to get products once the page has loaded
// window.onload = fetchProductData;
