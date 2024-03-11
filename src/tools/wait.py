from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging

import logging
import time

setup_logging()
logger = logging.getLogger()


def wait() -> str:
    """
    Waits for 5 seconds and returns a response string with the result of the action and the current URL.

    Args:
        None

    Returns:
        str: A response string stating the success of the action and the current URL.
    """

    try:
        webdriver = WebDriver.getInstance()
        driver = webdriver.getDriver()

        logger.info("Waiting 5 seconds...")
        time.sleep(5)

        return "Success. Waited 5 seconds. Current URL is: " + driver.url
    except Exception as e:
        logger.error("An error occurred while waiting: %s", str(e))
        return "Error occurred while waiting. Please check the logs for more details."
