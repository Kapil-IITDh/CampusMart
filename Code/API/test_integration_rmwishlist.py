from httpcore import TimeoutException
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "http://127.0.0.1:5502/Code/Frontend/index.html"  # Update this to your local frontend URL

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()



def login_user(driver, email, password):
    """Helper function to log in a user."""
    driver.get(BASE_URL.replace("index.html", "SignIn.html"))
    wait = WebDriverWait(driver, 10)

    # Enter email and password
    driver.find_element(By.ID, "email").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password)

    # Click the login button
    login_button = driver.find_element(By.CLASS_NAME, "signin-btn")
    login_button.click()
    alert = wait.until(EC.alert_is_present())
    alert.accept() 
    # Wait for login confirmation and check local storage
    wait.until(EC.url_contains("index.html"))
    assert "index.html" in driver.current_url, "Login failed - did not navigate to index.html"
    print("Login successful")



def test_remove_from_wishlist(driver):
    login_user(driver, "user2@iitdh.ac.in", "user2")
    wait = WebDriverWait(driver, 10)

    # Navigate to wishlist page
    driver.get(BASE_URL.replace("index.html", "wishlist.html"))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wishlist-item")))

    # Check that at least one product is in the wishlist
    initial_wishlist_count = len(driver.find_elements(By.CLASS_NAME, "wishlist-item"))
    assert initial_wishlist_count > 0, "No products in wishlist to remove."

    # Click the first remove button
    print("Attempting to find remove button...")
    remove_button = wait.until(EC.element_to_be_clickable((By.ID, "removeFromWishlistButton")))
    print("Remove button found, clicking it.")
    remove_button.click()

    try:
        print("Waiting for alert to appear...")
        alert = WebDriverWait(driver, 20).until(EC.alert_is_present())
        print("Alert appeared with text:", alert.text)
        alert.accept()
    except TimeoutException:
        print("Alert did not appear within the wait time.")
        assert False, "Expected alert did not appear after clicking remove button."


    # Verify product count in wishlist decreased
    print("Wishlist removal test completed successfully")
