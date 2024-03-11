from src.webdriver.webdriver import WebDriver


driver_instance = WebDriver.getInstance()
driver = driver_instance.getDriver()
driver.goto("https://www.google.com")
