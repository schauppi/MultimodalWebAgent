from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging

import logging

setup_logging()
logger = logging.getLogger(__name__)


def read_url(url: str) -> str:
    """
    Reads the content of a URL using a WebDriver instance adapted for Playwright, 
    executes a script to remove popups, and returns the current URL.

    Args:
        url (str): The URL to read.

    Returns:
        str: The current URL.
    """
    try:
        if not url.startswith('https://'):
            url = 'https://' + url

        logger.info(f"Reading URL: {url}")
        driver_instance = WebDriver.getInstance()
        driver = driver_instance.getDriver()
        driver.goto(url)

        return "Current URL is: " + driver.url + "\n"
    except Exception as e:
        logger.error(f"Failed to read URL {url}: {e}")
        raise
