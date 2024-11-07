{/* <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script> */}

console.log("SignUp.js loaded successfully");

async function registerUser() {
    // Prevent the form from submitting in the traditional way
    console.log('registerUser function called');

    // Get form values
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const department = document.getElementById("department").value;
    const userType = document.getElementById("userType").value;
    const phoneNumber = document.getElementById("phoneNumber").value;

    // Check if a user type is selected
    if (!userType) {
        alert("Please select a user type.");
        return;
    }

    // Hash the password using SHA-256
    // const hashedPassword = CryptoJS.SHA256(password).toString();
    hashedPassword = password;

    // Create a JSON object for the user data
    const userJSON = {
        name: name,
        email: email,
        department: department,
        password: hashedPassword,  // Hashed password
        userType: userType,
        phoneNumber: phoneNumber
    };

    try {
        // Make a POST request to the /register API
        const response = await fetch('http://127.0.0.1:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userJSON)
        });

        // Handle the response
        if (response.ok) {
            const result = await response.json();
            alert(result.message);  // Display success message
            localStorage.setItem('isLoggedIn', '1');
            console.log('User signed in and stored in localStorage.');
            window.location.href = "./index.html";
        } else {
            const errorResult = await response.json();
            alert(`Registration failed: ${errorResult.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred during registration. Please try again.");
    }
}

function hola() {
    alert("new");
}