// Check if user data is available in localStorage
const storedUserData = localStorage.getItem('user');

if (storedUserData) {
    const userData = JSON.parse(storedUserData); // Parse the JSON string

    // Populate the HTML elements with the user data
    document.getElementById("name").value = userData.name || '';
    document.getElementById("email").value = userData.email || '';
    document.getElementById("phone").value = userData.phoneNumber || '';
    document.getElementById("password").value = "";

    console.log('User data loaded from localStorage:', userData);
} else {
    console.error('No user data found in localStorage.');
    alert('No user data found. Please log in.');
    window.location.href = "SignIn.html"; // Redirect to sign-in page if no data is found
}

// Function to handle user logout
function signOut() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('user');
    alert('Logged out successfully.');
    window.location.href = "SignIn.html";
}