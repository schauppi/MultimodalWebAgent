
from src.tools.read_url import read_url
from src.tools.utils.highlight_elements import highlight_elements
from src.tools.utils.get_webdriver_instance import get_webdriver_instance
from src.tools.utils.get_b64_screenshot import get_b64_screenshot

import time

url = "https://www.globalsqa.com/demo-site/select-dropdown-menu/"

read_url(url)

time.sleep(1)

driver = get_webdriver_instance()

time.sleep(1)

bbox_descriptions, bbox_coordinates, driver = highlight_elements(driver, "dropdown")

time.sleep(1)

screenshot = get_b64_screenshot(driver)
