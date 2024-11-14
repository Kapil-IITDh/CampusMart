import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

@pytest.fixture
def driver():
    # Setup Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5502/Code/Frontend/SignUp.html")  # Update with your actual signup page URL
    yield driver
    driver.quit()

def test_register_user(driver):
    print("Test for register user started")

    # Wait until the name field is present to ensure the page is fully loaded
    wait = WebDriverWait(driver, 10)
    name_field = wait.until(EC.presence_of_element_located((By.ID, "name")))

    # Fill in the form fields
    name_field.send_keys("Test User")
    driver.find_element(By.ID, "email").send_keys("testusr6@iitdh.ac.in")
    driver.find_element(By.ID, "password").send_keys("TestPass123")
    driver.find_element(By.ID, "department").send_keys("Engineering")
    driver.find_element(By.ID, "userType").send_keys("Student")
    driver.find_element(By.ID, "phoneNumber").send_keys("1234567890")

    # Submit the form
    print("Submitting the form")
    driver.find_element(By.ID, "signup-btn").send_keys(Keys.RETURN)

    # Wait for the alert and verify its text
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print("Alert message received:", alert_text)
        assert "User registered successfully" in alert_text  # Replace with actual success message
        alert.accept()
    except Exception as e:
        print("Error during registration:", e)
        assert False, "Alert not found or unexpected alert message."

    # Verify redirection to the homepage
    print("Checking if redirected to the homepage")
    wait.until(EC.url_to_be("http://127.0.0.1:5502/Code/Frontend/index.html"))  # Adjust to your actual URL
    assert driver.current_url == "http://127.0.0.1:5502/Code/Frontend/index.html"
    print("Test for register user completed successfully")


