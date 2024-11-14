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

def test_add_product_to_wishlist(driver):
    # Log in before performing other actions
    login_user(driver, "user2@iitdh.ac.in", "user2")

    # Load the products page
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    # Wait for the product blocks to appear
    product_blocks = wait.until(lambda d: d.find_elements(By.CLASS_NAME, "productBlock"))
    assert len(product_blocks) > 0, "No products displayed on the page."

    # Click on the first product to view details
    first_product = product_blocks[0]
    first_product.click()

    # Wait until we're on the product details page
    wait.until(EC.url_contains("product.html"))
    assert "product.html" in driver.current_url, "Failed to navigate to product details page."

    # Click on "Add to Wishlist" button
    add_to_wishlist_button = wait.until(EC.presence_of_element_located((By.ID, "addToWishlistButton")))
    add_to_wishlist_button.click()

    # Check for success alert for wishlist addition
    alert = wait.until(EC.alert_is_present())
    alert_text = alert.text
    assert "Product added to wishlist successfully" in alert_text, "Failed to add product to wishlist."
    alert.accept()  # Close the alert

    print("Wishlist addition test completed successfully.")

def test_make_offer_navigates_to_message(driver):
    # Log in before performing other actions
    login_user(driver, "user2@iitdh.ac.in", "user2")

    # Navigate back to the products list page
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)

    # Wait for the product blocks to appear
    product_blocks = wait.until(lambda d: d.find_elements(By.CLASS_NAME, "productBlock"))
    assert len(product_blocks) > 0, "No products displayed on the page."

    # Click on the first product to view details
    first_product = product_blocks[0]
    first_product.click()

    # Wait until we're on the product details page
    wait.until(EC.url_contains("product.html"))
    assert "product.html" in driver.current_url, "Failed to navigate to product details page."

    # Click on "Make Offer" button
    make_offer_button = wait.until(EC.presence_of_element_located((By.ID, "makeOfferButton")))
    make_offer_button.click()

    # Verify navigation to messaging page with listingID
    wait.until(EC.url_contains("message.html"))
    assert "message.html" in driver.current_url, "Failed to navigate to messaging page."

    # Check if listingID is in the URL
    assert "seller_id=" in driver.current_url, "listingID parameter missing in message page URL."

    print("Make offer navigation test completed successfully.")
