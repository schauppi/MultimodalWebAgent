from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging
from src.tools.utils.get_b64_screenshot import get_b64_screenshot
from src.tools.utils.vision_template import get_vision_template
from src.tools.utils.analyze_image import analyze_image
from src.tools.utils.load_context import load_context
from src.tools.utils.get_webdriver_instance import get_webdriver_instance

import logging

setup_logging()
logger = logging.getLogger()


def analyze_content(query: str) -> str:
    """
    Analyzes the content of a webpage based on a screenshot and a user query, and returns a response string with insights and answers.

    Args:
        query (str): A query string representing the user's inquiry about the contents of the current web browser window.

    Returns:
        str: A response string providing insights and answers regarding the information presented in the active browser window.
    """
    try:
        logger.info("Initializing WebDriver to capture a webpage screenshot.")
        driver = get_webdriver_instance()

        screenshot_b64 = get_b64_screenshot(driver)

        context = load_context("analyze_content")

        logger.info("Generating message history for image analysis.")
        message_history = get_vision_template(context, screenshot_b64, query)

        logger.info("Analyzing the webpage screenshot.")
        message = analyze_image(message_history)

        return message
    except Exception as e:
        logger.error("Failed to analyze content.", exc_info=True)
        return "An error occurred while analyzing the webpage content. Please try again later."
