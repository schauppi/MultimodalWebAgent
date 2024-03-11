from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging
from src.tools.utils.get_webdriver_instance import get_webdriver_instance

import logging
import time

setup_logging()
logger = logging.getLogger()


def go_back() -> str:
    """
    Navigates back one page in the browser history using a WebDriver instance, and returns a response string with the result of the action.

    Args: 
        None

    Returns:
        str: A response string stating the success of the action and the current URL.
    """

    try:
        driver = get_webdriver_instance()

        logger.info("Navigating back 1 page...")
        driver.go_back()

        time.sleep(3)

        return "Success. Went back 1 page. Current URL is: " + driver.url
    except Exception as e:
        logger.error("An error occurred while navigating back: %s", str(e))
        return "Error occurred while navigating back. Please check the logs for more details."
