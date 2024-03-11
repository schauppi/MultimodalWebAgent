from src.configs.logging.logging_config import setup_logging

import logging
import os
import base64

setup_logging()
logger = logging.getLogger()


def save_screenshot_to_file(screenshot_b64: str, folder_path: str = "src/data/screenshots") -> str:
    """
    Saves a base64 encoded screenshot to a PNG file.

    Args:
        screenshot_b64 (str): The base64 encoded screenshot.
        folder_path (str): The folder path where the screenshot will be saved.

    Returns:
        str: The path to the saved screenshot file.
    """
    try:
        if not os.path.exists(folder_path):
            logger.info(f"Creating directory {folder_path}.")
            os.makedirs(folder_path)

        count = len(os.listdir(folder_path)) + 1
        file_path = os.path.join(folder_path, f"{count}.png")

        with open(file_path, "wb") as file:
            logger.info(f"Saving screenshot to {file_path}.")
            file.write(base64.b64decode(screenshot_b64))

        return file_path
    except Exception as e:
        logger.error(f"Error saving screenshot: {str(e)}")
        return ""
