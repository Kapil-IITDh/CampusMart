import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5502/Code/Frontend/Sell.html")  # Update the path as per your setup
    yield driver
    driver.quit()

def test_sell_product(driver):
    print("Starting sell product test")

    # Define a wait to handle loading time
    wait = WebDriverWait(driver, 10)

    # Get form fields and fill them
    print("Filling out the form fields")

    # Check if the page has loaded by confirming the presence of the form title
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
    
    # Fill in product title
    driver.find_element(By.ID, "title").send_keys("Test Product")

    # Fill in selling price
    driver.find_element(By.ID, "selling_price").send_keys("50")

    # Fill in new item price
    driver.find_element(By.ID, "new_item_price").send_keys("100")

    # Fill in description
    driver.find_element(By.ID, "description").send_keys("This is a description of the test product.")

    # Fill in grade
    driver.find_element(By.ID, "grade").send_keys("4")

    # Select a category (choose "Electronics" for example)
    category_dropdown = driver.find_element(By.ID, "categoryID")
    category_dropdown.click()
    driver.find_element(By.XPATH, "//select[@id='categoryID']/option[@value='1']").click()  # Value "1" for Electronics

    # Fill in image links
    driver.find_element(By.ID, "imageLinks").send_keys("https://example.com/image1.jpg\nhttps://example.com/image2.jpg")

    # Click the "Sell" button
    print("Submitting the form")
    driver.find_element(By.CLASS_NAME, "sell-btn").click()

    # Wait for the alert
    try:
        alert = wait.until(EC.alert_is_present())
        alert_text = alert.text
        print("Alert received:", alert_text)

        # Check for two possible alert messages
        if "Product listed successfully" in alert_text:
            print("Success: Product listed successfully")
            alert.accept()

            # Confirm form reset after successful listing
            title_value = driver.find_element(By.ID, "title").get_attribute("value")
            assert title_value == "", "Form was not reset after submission"
            print("Form reset verified after successful listing")

        elif "User not logged in" in alert_text:
            print("Warning: User is not logged in.")
            alert.accept()

            # Verify that no further action was taken by checking form values are unchanged
            title_value = driver.find_element(By.ID, "title").get_attribute("value")
            assert title_value == "Test Product", "Form data should remain after 'User not logged in' alert"
            print("Form data retention verified for 'User not logged in' scenario")

        else:
            print("Unexpected alert message:", alert_text)
            assert False, "Unexpected alert message"

    except Exception as e:
        print("Error or no alert received:", e)
        assert False, "Expected alert did not appear"
        
    print("Sell product test completed successfully")
