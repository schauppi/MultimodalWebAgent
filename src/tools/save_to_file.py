from src.configs.logging.logging_config import setup_logging

import logging
import os
import datetime

setup_logging()
logger = logging.getLogger()


def save_to_file(data: str) -> None:
    """
    Saves the data to a file.

    Args:
        data (str): The data to save to the file.

    Returns:
        None
    """
    try:
        base_folder = 'src/data/saved_data/'
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)
        os.chdir(base_folder)
        folder_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(folder_name)
        file_name = folder_name + "/data.txt"
        with open(file_name, "w") as file:
            file.write(data)

        logger.info(f"Data saved to file: {file_name}")
    except Exception as e:
        logger.error(f"Error saving data to file: {str(e)}")
    return None
