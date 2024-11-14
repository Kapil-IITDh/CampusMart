import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

@pytest.fixture
def driver():
    # Setup Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5502/Code/Frontend/SignIn.html")  # Updated path for SignIn page
    yield driver
    driver.quit()

def test_sign_in_user(driver):
    print("Test for sign-in user started")

    # Define WebDriverWait with a 10-second timeout
    wait = WebDriverWait(driver, 10)

    # Find and fill out the email field
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    email_field.send_keys("user2@iitdh.ac.in")

    # Find and fill out the password field
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("user2")  # Use a test password

    # Submit the form by clicking the Sign in button
    print("Submitting the form")
    driver.find_element(By.CLASS_NAME, "signin-btn").click()

    # Wait for alert and verify message for successful login
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print("Alert message received:", alert_text)
        assert "Login successful" in alert_text  # Replace with your actual success message in response
        alert.accept()
    except Exception as e:
        print("Error during login:", e)
        assert False, "Login alert not found or unexpected alert message."

    # Check for redirection to index page after login
    print("Checking redirection after login")
    wait.until(EC.url_to_be("http://127.0.0.1:5502/Code/Frontend/index.html"))  # Updated expected URL after login
    assert driver.current_url == "http://127.0.0.1:5502/Code/Frontend/index.html"

    print("Test for sign-in user completed successfully")


