import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Base URL to be updated with your frontend server location
BASE_URL = "http://127.0.0.1:5502/Code/Frontend/index.html"

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def test_product_fetch_and_display(driver):
    # Load the index page
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 10)
    print("Testing product fetch and display started.")

    # Wait for the product container to load
    product_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "productBlockContainer")))
    assert product_container is not None, "Product container did not load."

    # Wait for products to be populated in the container
    product_blocks = wait.until(lambda d: d.find_elements(By.CLASS_NAME, "productBlock"))
    assert len(product_blocks) > 0, "No products were displayed on the page."

    # Validate the first product block details
    first_product = product_blocks[0]
    title = first_product.find_element(By.CLASS_NAME, "productTitle").text
    price = first_product.find_element(By.CLASS_NAME, "productPrice").text
    image = first_product.find_element(By.TAG_NAME, "img")
    image_src = image.get_attribute("src")

    # Confirm product title and price are displayed and not empty
    assert title != "", "Product title is empty."
    assert price.startswith("₹"), "Product price format is incorrect."
    assert "http" in image_src, "Image URL is not valid."

    # Log the retrieved values for debugging
    print(f"First product title: {title}")
    print(f"First product price: {price}")
    print(f"First product image URL: {image_src}")

    # Test that clicking the first product navigates to product page
    first_product.click()
    wait.until(EC.url_contains("product.html"))
    assert "product.html" in driver.current_url, "Did not navigate to product.html as expected."

    print("Product fetch, display, and navigation test completed successfully.")
