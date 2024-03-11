from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging
from src.tools.utils.get_webdriver_instance import get_webdriver_instance

import logging
import time

setup_logging()
logger = logging.getLogger()


def jump_to_search_engine() -> str:
    """
    Navigates to the Google search engine using a WebDriver instance, and returns a response string with the result of the action.

    Args:
        None

    Returns:
        str: A response string stating the success of the action and the current URL.
    """

    try:
        driver = get_webdriver_instance()

        driver.goto("https://www.google.com")

        time.sleep(3)

        logger.info(
            "Success. Jumped to Google search engine. Current URL is: " + driver.url)
        return "Success. Jumped to Google search engine. Current URL is: " + driver.url

    except Exception as e:
        logger.error("An error occurred: " + str(e))
        return "An error occurred: " + str(e)
