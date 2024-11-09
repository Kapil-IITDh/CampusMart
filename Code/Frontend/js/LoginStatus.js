
function updateLoginStatus(isLoggedIn) {
    const loginLink = document.getElementById('loginLink');
    const navbarSecond = document.getElementById('NavbarSecond');
    

    if (isLoggedIn) {
        loginLink.textContent = 'Profile';
        loginLink.href = './profile.html';
        navbarSecond.style.display = 'block'; // Show the second navbar
    } else {
        loginLink.textContent = 'Sign in';
        loginLink.href = './SignIn.html';
        navbarSecond.style.display = 'none'; // Hide the second navbar
    }
}

// Function to sign in the user and store the login status in localStorage
function signIn() {
    localStorage.setItem('isLoggedIn', '1');
    updateLoginStatus(true);
    console.log('User signed in and stored in localStorage.');
}

// Function to sign out the user and remove the login status from localStorage
function signOut() {
    localStorage.removeItem('isLoggedIn');
    updateLoginStatus(false);
    console.log('User signed out and removed from localStorage.');
    window.location.href = "./index.html"
    
}
