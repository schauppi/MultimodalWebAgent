from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging
from src.tools.utils.get_webdriver_instance import get_webdriver_instance

import logging
import time
from typing import Literal

setup_logging()
logger = logging.getLogger()


def scroll(direction: Literal["up", "down"]) -> str:
    """
    Scrolls the current page up or down by 500 pixels.

    Args:
        direction (Literal["up", "down"]): The direction to scroll.

    Returns:
        str: A message confirming the scroll action.
    """

    try:
        if direction not in ["up", "down"]:
            raise ValueError("Direction must be either 'up' or 'down'.")

        driver = get_webdriver_instance()

        scroll_amount = 500
        if direction == "up":
            driver.evaluate(f"window.scrollBy(0, {-scroll_amount})")
        else:
            driver.evaluate(f"window.scrollBy(0, {scroll_amount})")

        time.sleep(2)

        logger.info(f"Scrolled {direction} by {scroll_amount} pixels.")
        return f"Scrolled {direction} by {scroll_amount} pixels."

    except Exception as e:
        logger.error(f"Failed to scroll {direction}: {e}")
        raise
