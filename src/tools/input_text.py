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


def input_text(query: str) -> str:
    """
    Interacts with a webpage by sending keys to input fields based on a provided query, 
    and returns a response string with the result of the action or an error message.

    Args:
        query (str): The query to be used for identifying the input fields and the keys to be sent.

    Returns:
        str: A response string with the result of the action or an error message.
    """

    pass
