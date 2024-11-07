document.addEventListener("DOMContentLoaded", function () {
    // Define the base URL for the project
    const baseUrl = window.location.origin;

    // Load the first navbar
    fetch(baseUrl + '/Code/Frontend/partials/NavbarFirst.html')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load NavbarFirst.html');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('NavbarFirst').innerHTML = data;
            // After loading the first navbar, check login status
            checkLoginStatus();
        })
        .catch(error => console.error('Error loading NavbarFirst:', error));

    // Load the second navbar
    fetch(baseUrl + '/Code/Frontend/partials/NavbarSecond.html')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load NavbarSecond.html');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('NavbarSecond').innerHTML = data;
        })
        .catch(error => console.error('Error loading NavbarSecond:', error));

    // Load the footer
    fetch(baseUrl + '/Code/Frontend/partials/Footer.html')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load Footer.html');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('Footer').innerHTML = data;
        })
        .catch(error => console.error('Error loading Footer:', error));
});

// Function to check login status and update the UI
function checkLoginStatus() {
    const isLoggedIn = localStorage.getItem('isLoggedIn') === '1';
    updateLoginStatus(isLoggedIn);
}

// Update login/logout UI based on login status
function updateLoginStatus(isLoggedIn) {
    const navbarSecond = document.getElementById('NavbarSecond');
    
    // Update NavbarSecond based on login status
    if (isLoggedIn) {
        // Show signed-in state
        navbarSecond.innerHTML = `<button onclick="signOut()">Sign Out</button>`;
    } else {
        // Show sign-in button
        navbarSecond.innerHTML = `<button onclick="signIn()">Sign In</button>`;
    }
}

// Sign-in function
function signIn() {
    // Here, simulate the login process
    localStorage.setItem('isLoggedIn', '1');
    checkLoginStatus(); // Update the UI
    console.log('User signed in');
}

// Sign-out function
function signOut() {
    // Simulate the logout process
    localStorage.removeItem('isLoggedIn');
    checkLoginStatus(); // Update the UI
    console.log('User signed out');
}
