console.log("SignUp.js loaded successfully");

async function registerUser() {
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

    // Hash the password (commented out for simplicity)
    // const hashedPassword = CryptoJS.SHA256(password).toString();
    const hashedPassword = password; // Replace with the hashing if needed

    // Create a JSON object for the user data
    const userJSON = {
        name: name,
        email: email,
        department: department,
        password: hashedPassword,
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
            
            // Store user data in localStorage
            localStorage.setItem('user', JSON.stringify(result.user));
            localStorage.setItem('isLoggedIn', '1');

            console.log('User data stored in localStorage:', result.user);
            // alert(result.user.userID);
            window.userID = result.user.userID;
            // Redirect to the homepage or another page
            window.location.href = "./index.html";
        } else {
            const errorResult = await response.json();
            // alert(`Registration failed: ${errorResult.error}`);
        }
    } catch (error) {
        console.error('Error:', error);
        // alert("An error occurred during registration. Please try again.");
    }
}

// Helper function to check user ID
function getUserId() {
    const user = JSON.parse(localStorage.getItem('user'));
    window.userId =  user.userID ;
    return user ? user.userID : null;
}

function hola() {
    // alert("new");
}
