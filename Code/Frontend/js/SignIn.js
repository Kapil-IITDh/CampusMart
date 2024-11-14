console.log("SignIn.js loaded successfully");

async function signIn() {
    // Prevent form submission behavior
    // event.preventDefault();

    // Get form values
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Hash the password (commented for simplicity)
    // const hashedPassword = CryptoJS.SHA256(password).toString();
    const hashedPassword = password; // Use this if hashing is not needed

    // Create the JSON object to send
    const userJSON = {
        email: email,
        password: hashedPassword  // Send the hashed password
    };

    try {
        // Send a POST request to the login endpoint
        const response = await fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userJSON)
        });

        if (response.ok) {
            const result = await response.json();
            alert(result.message);  // Display a success message

            // Store user information in localStorage or sessionStorage
            localStorage.setItem('isLoggedIn', '1');
            localStorage.setItem('user', JSON.stringify(result.user));  // Store user details
            console.log('User data stored in localStorage:', result.user);
            
            window.userID = result.user.userID;
            // alert(window.userID);
            // Redirect to the homepage or another page
            window.location.href = "./index.html";
        } else {
            const errorResult = await response.json();
            alert(errorResult.message);  // Show an alert for invalid credentials
        }
    } catch (error) {
        console.error('Error:', error);
        alert("An error occurred during login. Please try again.");
    }
}

// Function to access the logged-in user's ID from localStorage
function getUserId() {
    const user = JSON.parse(localStorage.getItem('user'));
    return user ? user.userID : null;
}
