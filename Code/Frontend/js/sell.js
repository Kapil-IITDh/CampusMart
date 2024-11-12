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

async function uploadImages() {
    // Check if userID is available
    if (!userID) {
        alert("User not logged in. Please log in to list a product.");
        return false;
    }

    // Collect form data
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const sellingPrice = parseFloat(document.getElementById("selling_price").value);
    const newItemPrice = document.getElementById("new_item_price").value ? parseFloat(document.getElementById("new_item_price").value) : null;
    const categoryID = parseInt(document.getElementById("categoryID").value);
    const grade = parseInt(document.getElementById("grade").value);
    const imageLinks = document.getElementById("imageLinks").value.split('\n').map(link => link.trim()).filter(link => link);

    alert(title,description,sellingPrice,newItemPrice,categoryID,grade,imageLinks);
      // Validation check for empty fields
      if (!title) {
        alert("Please enter a title.");
        return false;
    }
    if (!description) {
        alert("Please enter a description.");
        return false;
    }
    if (!sellingPrice || isNaN(parseFloat(sellingPrice))) {
        alert("Please enter a valid selling price.");
        return false;
    }
    if (newItemPrice && isNaN(parseFloat(newItemPrice))) {
        alert("Please enter a valid new item price or leave it empty.");
        return false;
    }
    if (!categoryID || isNaN(parseInt(categoryID))) {
        alert("Please select a valid category.");
        return false;
    }
    if (!grade || isNaN(parseInt(grade)) || parseInt(grade) < 1 || parseInt(grade) > 5) {
        alert("Please enter a valid grade between 1 and 5.");
        return false;
    }
    if (imageLinks.length < 1) {
        alert("Please provide at least 1 image URLs.");
        return false;
    }
    // Prepare data for the API call
    const listingData = {
        userID: userID,
        title: title,
        description: description,
        selling_price: sellingPrice,
        new_item_price: newItemPrice,
        categoryID: categoryID,
        grade: grade,
        imageLinks: imageLinks
    };

    try {
        // Make the API call to add the listing
        const response = await fetch('http://127.0.0.1:5000/add_listing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(listingData)
        });

        // Handle the API response
        if (response.ok) {
            const result = await response.json();
            alert(`Product listed successfully! Listing ID: ${result.listingID}`);
            document.getElementById("sellForm").reset(); // Reset the form
        } else {
            const error = await response.json();
            alert(`Failed to list product: ${error.message || "Please try again."}`);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while listing the product.");
    }

    // Return false to prevent form submission if this function is used directly in HTML form `onsubmit`
    return false;
}
