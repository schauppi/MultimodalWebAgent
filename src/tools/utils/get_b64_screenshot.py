from src.configs.logging.logging_config import setup_logging
from src.tools.utils.save_screenshot import save_screenshot_to_file
import base64
import os
import logging

setup_logging()
logger = logging.getLogger()


def get_b64_screenshot(driver, element=None) -> str:
    """
    Captures a screenshot of the current web page or a specific element and returns it as a base64 encoded string.

    Args:
        driver (Playwright Browser): The Playwright browser instance.
        element (Playwright ElementHandle, optional): The Playwright element handle. Defaults to None.

    Returns:
        str: A base64 encoded string representing the screenshot of the current web page or a specific element.
    """
    temp_file_path = "temp_screenshot.png"
    try:
        logger.info("Capturing screenshot")
        if element:
            screenshot = element.screenshot(
                path=temp_file_path, full_page=False)
        else:
            screenshot = driver.screenshot(
                path=temp_file_path, full_page=False)

        with open(temp_file_path, "rb") as image_file:
            screenshot = base64.b64encode(image_file.read()).decode("utf-8")

        os.remove(temp_file_path)

        _ = save_screenshot_to_file(screenshot)

        return screenshot
    except Exception as e:
        logger.error(f"Error occurred while capturing screenshot: {str(e)}")
        return ""
