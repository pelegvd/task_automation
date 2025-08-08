# main.py

import random
import string
import pytest
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def step(message):
    logger.info(message)
    print(message)

def generate_random_email():
    return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) + "@example.com"

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    yield driver
    driver.quit()

def test_register_and_add_product(driver):
    wait = WebDriverWait(driver, 15)
    try:
        step("Step 1: Opening the website...")
        driver.get("https://demowebshop.tricentis.com")
        time.sleep(2)

        step("Step 2: Clicking on 'Register'...")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register"))).click()
        time.sleep(1)

        step("Step 3: Filling in registration details...")
        gender_male = wait.until(EC.element_to_be_clickable((By.ID, "gender-male")))
        first_name = wait.until(EC.visibility_of_element_located((By.ID, "FirstName")))
        last_name = driver.find_element(By.ID, "LastName")
        email = driver.find_element(By.ID, "Email")
        password = driver.find_element(By.ID, "Password")
        confirm_password = driver.find_element(By.ID, "ConfirmPassword")
        email_value = generate_random_email()

        gender_male.click()
        first_name.send_keys("Peleg")
        last_name.send_keys("Vadbeker")
        email.send_keys(email_value)
        password.send_keys("Test1234$")
        confirm_password.send_keys("Test1234$")
        time.sleep(1)

        step("Step 4: Clicking on 'Register' button...")
        driver.find_element(By.ID, "register-button").click()
        time.sleep(1)

        step("Step 5: Clicking on 'Continue'...")
        wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue']"))).click()
        time.sleep(1)

        step("Step 6: Validating registration success...")
        header = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "account")))
        assert email_value in header.text, "Registration header doesn't contain the new email"
        step(f"✅ Registration successful with email: {email_value}")
        time.sleep(1)

        step("Step 7: Clicking on 'Digital downloads'...")
        wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Digital downloads"))).click()
        time.sleep(1)

        step("Step 8: Selecting a random product and adding to cart...")
        products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "product-item")))
        assert products, "No products found in Digital downloads"
        selected_product = random.choice(products)
        product_name = selected_product.find_element(By.CLASS_NAME, "product-title").text
        add_btn = selected_product.find_element(By.CLASS_NAME, "product-box-add-to-cart-button")
        wait.until(EC.element_to_be_clickable(add_btn)).click()
        step(f"🛒 Added product to cart: {product_name}")
        time.sleep(1)

        step("Step 9: Navigating to shopping cart...")
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cart-label"))).click()
        time.sleep(1)

        step("Step 10: Validating product in cart...")
        cart_product_name = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "product-name"))).text
        assert product_name in cart_product_name, "Product in cart does not match selected product"
        step(f"✅ Product verified in cart: {cart_product_name}")

    except Exception as e:
        logger.error(f"❌ Test failed at step: {e}", exc_info=True)
        print(f"❌ Test failed at step: {e}")
        raise
