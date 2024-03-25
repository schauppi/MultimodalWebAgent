
from src.tools.read_url import read_url
from src.tools.click_element import click_element
from src.tools.utils.highlight_elements import highlight_elements
from src.tools.utils.get_webdriver_instance import get_webdriver_instance
from src.tools.utils.get_b64_screenshot import get_b64_screenshot

import time

url = "https://www.globalsqa.com/demo-site/select-dropdown-menu/"

read_url(url)

time.sleep(5)

click_element("click on the dropdown menu to select the langauge")

time.sleep(5)

driver = get_webdriver_instance()

driver.keyboard.type("Austria")

time.sleep(5)
