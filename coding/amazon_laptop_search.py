# filename: amazon_laptop_search.py
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Initialize Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # Step 1: Go to the Amazon website
    driver.get("https://www.amazon.in")

    # Step 2: Search for 'laptop'
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("laptop")
    search_box.send_keys(Keys.ENTER)
    time.sleep(2)  # wait for the page to load

    # Step 3: Apply the More Than 4 Stars filter
    driver.find_element(By.CSS_SELECTOR, "a[href*='customerReviews=4']").click()
    time.sleep(2)  # wait for filter application

    # Step 4: Click on the first product
    driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.sg-col-inner")[0].click()
    time.sleep(2)  # wait for product page to load

    # Switching to the product tab if a new one was opened
    driver.switch_to.window(driver.window_handles[-1])
    
    # Step 5: Add the item to the cart
    driver.find_element(By.ID, "add-to-cart-button").click()
    time.sleep(2)  # wait for item to be added to the cart

    print("Successfully added the first laptop with more than 4 stars to the cart.")
except Exception as e:
    print("An error occurred:", str(e))
finally:
    driver.quit()