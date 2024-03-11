from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging
from src.tools.utils.get_webdriver_instance import get_webdriver_instance

import logging

setup_logging()
logger = logging.getLogger()


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
        driver = get_webdriver_instance()
        driver.goto(url)

        return "Current URL is: " + driver.url + "\n"
    except Exception as e:
        logger.error(f"Failed to read URL {url}: {e}")
        raise
