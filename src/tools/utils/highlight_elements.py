from src.webdriver.webdriver import WebDriver
from typing import Literal
import json
import logging

from src.configs.logging.logging_config import setup_logging
setup_logging()
logger = logging.getLogger()


def format_description(elements: list) -> tuple:
    """
    Formats the description of page elements and their bounding box coordinates.

    Args:
        elements (list): A list of element dictionaries with keys like 'ariaLabel', 'x', 'y', 'text'.

    Returns:
        tuple: A tuple containing a JSON string of elements' descriptions and a list of bounding box coordinates.
    """
    labels = []
    bbox_coordinates = []
    for i, bbox in enumerate(elements):
        text = bbox.get("ariaLabel") or ""
        bbox_coordinates.append((bbox.get("x"), bbox.get("y")))
        if not text.strip():
            text = bbox.get("text")
        labels.append({str(i):  text})

    bbox_descriptions = json.dumps(labels, indent=4)
    return bbox_descriptions, bbox_coordinates


def highlight_elements(driver, mark: Literal["click", "input", "all", "remove"]):
    """
    Highlights elements on a webpage based on the mark type.

    Args:
        driver (WebDriver): An instance of the WebDriver.
        mark (Literal["click", "input", "all", "remove"]): The type of elements to mark.

    Returns:
        A tuple containing descriptions and coordinates of marked elements or the driver itself after unmarking elements.
        In case of errors, it returns an error message.
    """
    if mark not in ["click", "input", "all", "remove"]:
        raise ValueError(
            "Mark must be either 'click', 'input', 'all' or 'remove'.")

    try:
        with open('src/tools/utils/mark_page.js') as f:
            mark_page_script = f.read()

        if mark == "click":
            elements = driver.evaluate(f"""() => {{
                {mark_page_script}
                return markClickableElements();
            }}""")
            bbox_descriptions, bbox_coordinates = format_description(elements)
            return bbox_descriptions, bbox_coordinates, driver
        elif mark == "input":
            elements = driver.evaluate(f"""() => {{
                {mark_page_script}
                return markInputElements();
            }}""")
            bbox_descriptions, bbox_coordinates = format_description(elements)
            return bbox_descriptions, bbox_coordinates, driver
        elif mark == "all":
            elements = driver.evaluate(f"""() => {{
                {mark_page_script}
                return markAllElements();
            }}""")
            bbox_descriptions, bbox_coordinates = format_description(elements)
            return bbox_descriptions, bbox_coordinates, driver
        else:
            driver.evaluate(f"""() => {{
                {mark_page_script}
                return unmarkPage();
            }}""")
            return driver
    except Exception as e:
        return str(e)
