console.log("hola");

function callFirstApi(){
    fetch("http://127.0.0.1:5000/")
    .then((res) => res.json())
    .then((data)=> document.getElementById("api-msg").textContent = data.message);
}


function allUsers(){
    fetch("http://127.0.0.1:5000/users")
    .then((res)=> res.json())
    .then(function (data){
        document.getElementById("uid").textContent = "User name : " + data[0].userID;
          document.getElementById("uname").textContent = "User id : " + data[0].name;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const categoryForm = document.getElementById('category-form');
    const productForm = document.getElementById('product-form');
    const viewCategoriesBtn = document.getElementById('view-categories-btn');
    const viewProductsBtn = document.getElementById('view-products-btn');
    const categoriesList = document.getElementById('categories-list');
    const productsList = document.getElementById('products-list');

    categoryForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const categoryName = document.getElementById('categoryName').value;
        
        const response = await fetch('http://127.0.0.1:5000/categories', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ categoryName })
        });

        if (response.ok) {
            alert('Category added successfully');
        } else {
            alert('Failed to add category');
        }
    });

    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const userID = document.getElementById('userID').value;
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const selling_price = document.getElementById('selling_price').value;
        const new_item_price = document.getElementById('new_item_price').value;
        const categoryID = document.getElementById('categoryID').value;
        const grade = document.getElementById('grade').value;
        const images = document.getElementById('images').value.split(',').map(img => img.trim());

        const response = await fetch('http://localhost:5000/product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ userID, title, description, selling_price, new_item_price, categoryID, grade, images })
        });

        if (response.ok) {
            alert('Product added successfully');
        } else {
            alert('Failed to add product');
        }
    });

    viewCategoriesBtn.addEventListener('click', async () => {
        const response = await fetch('http://localhost:5000/categories');
        const categories = await response.json();

        categoriesList.innerHTML = '';
        categories.forEach(category => {
            const li = document.createElement('li');
            li.textContent = category.categoryName;
            categoriesList.appendChild(li);
        });
    });

    viewProductsBtn.addEventListener('click', async () => {
        const response = await fetch('http://localhost:5000/products');
        const data = await response.json();
        const products = data.products;

        productsList.innerHTML = '';
        products.forEach(product => {
            const li = document.createElement('li');
            li.textContent = `${product.title} - $${product.selling_price}`;
            productsList.appendChild(li);
        });
    });
});
