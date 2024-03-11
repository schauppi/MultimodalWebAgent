from src.webdriver.webdriver import WebDriver
from src.configs.logging.logging_config import setup_logging
from src.tools.utils.highlight_elements import highlight_elements
from src.tools.utils.get_b64_screenshot import get_b64_screenshot
from src.tools.utils.vision_template import get_vision_template
from src.tools.utils.load_context import load_context
from src.tools.utils.analyze_image import analyze_image
from src.tools.utils.get_webdriver_instance import get_webdriver_instance

import logging
import time

setup_logging()
logger = logging.getLogger()


def click_element(query: str) -> str:
    """
    Clicks on a webpage element based on a user query, and returns a response string with the result of the action.

    Args:
        query (str): A query string representing the user's inquiry about the contents of the current web browser window.

    Returns:
        str: A response string providing insights and answers regarding the information presented in the active browser window.
    """
    try:
        driver = get_webdriver_instance()
        logger.info("Highlighting clickable elements on the page.")
        bbox_descriptions, bbox_coordinates, driver = highlight_elements(
            driver, "click")
        screenshot = get_b64_screenshot(driver)
        driver = highlight_elements(driver, "remove")
    except Exception as e:
        logger.error("Error highlighting elements: %s", e, exc_info=True)
        return "Failed to highlight clickable elements. Please check the logs for more details."

    try:
        click_template = load_context("click_template")
        enriched_query = f"{query}.\n\nText on all visible clickable elements: {bbox_descriptions}"
        message_history = get_vision_template(
            click_template, screenshot, enriched_query)
        return process_click(driver, message_history, bbox_coordinates, bbox_descriptions)
    except Exception as e:
        logger.error("Error processing click action: %s", e, exc_info=True)
        return "Failed to process click action. Please check the logs for more details."


def process_click(driver, message_history, bbox_coordinates, bbox_descriptions) -> str:
    """
    Processes the click action by analyzing the image and clicking the identified element.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        message_history (str): A string representing the message history for image analysis.
        bbox_coordinates (list): A list of bounding box coordinates.
        bbox_descriptions (str): A JSON string of elements' descriptions.

    Returns:
        str: A response string with the result of the click action.
    """
    for attempt in range(3):
        try:
            logger.info("Analyzing image to identify the clickable element.")
            message = analyze_image(message_history)
            if "none" in message.lower():
                return "No element found matching the description."
            element_index = int(''.join(filter(str.isdigit, message)))
            bbox = bbox_coordinates[element_index]
            return click_field(driver, bbox, bbox_descriptions, element_index)
        except Exception as e:
            logger.warning("Attempt %d: %s", attempt + 1, e, exc_info=True)
            if attempt == 2:  # Last attempt
                return "Failed to click on the element after several attempts."
    return "Failed to process click action."


def click_field(driver, bbox, bbox_descriptions, element) -> str:
    """
    Executes the click action on the specified element.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        bbox (tuple): A tuple containing the x and y coordinates of the element.
        bbox_descriptions (str): A JSON string of elements' descriptions.
        element (int): The index of the element to click.

    Returns:
        str: A response string with the result of the click action.
    """
    try:
        driver.mouse.click(bbox[0], bbox[1])
        time.sleep(3)  # Wait for potential page changes
        logger.info("Clicked on element: %s", bbox_descriptions[element])
        return f"Clicked on element {element}. Text on clicked element: '{bbox_descriptions[element]}'. Current URL is {driver.url}."
    except Exception as e:
        logger.error("Error during click action: %s", e, exc_info=True)
        return "Failed to click on the element. Please check the logs for more details."
