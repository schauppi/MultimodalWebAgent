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
import json
import platform

setup_logging()
logger = logging.getLogger(__name__)


def input_text(query: str) -> str:
    """
    Sends keys to input fields based on a query and returns a result or error message.

    Args:
        query (str): A string representing the user's input text query.

    Returns:
        str: A response string indicating the success or failure of the input action.
    """
    try:
        driver = get_webdriver_instance()
        logger.info("Highlighting input elements on the page.")
        bbox_descriptions, bbox_coordinates, driver = highlight_elements(
            driver, "input")
        screenshot = get_b64_screenshot(driver)
        highlight_elements(driver, "remove")
    except Exception as e:
        logger.error("Error highlighting input elements: %s", e, exc_info=True)
        return "Failed to highlight input elements. Please check the logs for more details."

    try:
        input_template = load_context("input_template")
        enriched_query = f"{query}.\n\nText on all visible input elements: {bbox_descriptions}"
        message_history = get_vision_template(
            input_template, screenshot, enriched_query)
        return process_input(driver, message_history, bbox_coordinates)
    except Exception as e:
        logger.error("Error processing input action: %s", e, exc_info=True)
        return "Failed to process input action. Please check the logs for more details."


def process_input(driver, message_history, bbox_coordinates) -> str:
    """
    Identifies input fields from an image and attempts to fill them.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        message_history (str): A string representing the message history for image analysis.
        bbox_coordinates (list): A list of bounding box coordinates for input elements.

    Returns:
        str: A response string indicating the success or failure of the input action.
    """
    for attempt in range(3):
        try:
            logger.info("Analyzing the image to identify input fields.")
            message = analyze_image(message_history)
            if "none" in message.lower():
                return "No matching element found. Use AnalyzeContent tool for further analysis."
            input_elements = extract_input_elements(message)
            fill_input_fields(driver, input_elements, bbox_coordinates)
            return f"Inserted text into the following elements: {list(input_elements.keys())}"
        except Exception as e:
            logger.warning(f"Attempt {attempt+1}: {e}", exc_info=True)
            if attempt == 2:  # Last attempt
                return "Failed to input text after several attempts."
    return "Failed to input text. Use AnalyzeContent tool for further analysis."


def extract_input_elements(message: str) -> dict:
    """
    Extracts input elements from a message.

    Args:
        message (str): A string representing the message from image analysis.

    Returns:
        dict: A dictionary containing input elements and their corresponding values.
    """
    logger.info("Extracting input elements from the message.")
    try:
        start = message.find('```json') + len('```json\n')
        end = message.rfind('```')
        json_str = message[start:end].strip()
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        logger.error("Error parsing JSON from message: %s", e, exc_info=True)
        raise


def fill_input_fields(driver, input_elements, bbox_coordinates) -> None:
    """
    Fills identified input fields with the provided values.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        input_elements (dict): A dictionary containing input elements and their corresponding values.
        bbox_coordinates (list): A list of bounding box coordinates for input elements.

    Returns:
        None
    """
    logger.info("Filling input fields with provided values.")
    try:
        for key, value in input_elements.items():
            bbox = bbox_coordinates[int(key)]
            click_and_fill(driver, bbox, str(value))
        logger.info("Input successfully completed.")
    except Exception as e:
        logger.error("Error during input: %s", e, exc_info=True)
        raise


def click_and_fill(driver, bbox, text):
    """
    Clicks on an input field and fills it with text.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        bbox (tuple): A tuple containing the x and y coordinates of the input field.
        text (str): A string representing the text to fill in the input field.

    Returns:
        None
    """
    driver.mouse.click(bbox[0], bbox[1])
    select_all_shortcut = "Meta+A" if platform.system() == "Darwin" else "Control+A"
    driver.keyboard.press(select_all_shortcut)
    time.sleep(1)
    driver.keyboard.press("Backspace")
    time.sleep(1)
    driver.keyboard.type(text)
    time.sleep(1)
    driver.keyboard.press("Enter")
    time.sleep(1)
    logger.info(f"Filled input field with text: {text}")
