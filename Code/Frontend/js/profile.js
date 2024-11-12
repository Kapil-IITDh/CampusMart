// Check if user data is available in localStorage
const storedUserData = localStorage.getItem('user');
const userID = getUserId();
// Function to retrieve the logged-in user ID from local storage
function getUserId(){
    const user = localStorage.getItem('user');
    if (user) {
        const userData = JSON.parse(user);
        console.log('User ID:', userData.userID);
        return userData.userID;
    } else {
        console.log('No user data found in localStorage.');
    }
}


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

async function loadUserRating() {
    // Retrieve user data from localStorage
    const user = JSON.parse(localStorage.getItem('user'));
    const userID = user ? user.userID : null;

    // Check if userID is available
    if (!userID) {
        document.getElementById('ratingBox').textContent = "User not logged in.";
        return;
    }

    // Fetch the average rating for the user
    try {
        const response = await fetch(`http://127.0.0.1:5000/user/average_rating?rateeID=${userID}`);
        if (!response.ok) {
            throw new Error("Failed to fetch user rating");
        }

        const data = await response.json();
        const ratingBox = document.getElementById('ratingBox');

        // Display the rating or a message if no ratings are available
        if (data.average_rating !== null) {
            ratingBox.textContent = `${data.average_rating} stars`;
        } else {
            ratingBox.textContent = "No Ratings";
        }

    } catch (error) {
        console.error("Error fetching user rating:", error);
        document.getElementById('ratingBox').textContent = "Unable to load rating";
    }
}

window.onload = function () {
    loadUserRating();
};
