from src.configs.logging.logging_config import setup_logging

import logging
import json
import datetime

setup_logging()
logger = logging.getLogger()


def load_assistant_id():
    """
    Load the assistant ID from the assistant ID file.

    Args:
    - None

    Returns:
    - assistant_id (str): The assistant ID. 
    """
    try:
        with open("src/data/assistant_id.json", "r") as file:
            data = json.load(file)
            latest_entry = max(data, key=lambda x: datetime.datetime.strptime(
                x['date'], "%Y-%m-%d %H:%M:%S.%f"))
            assistant_id = latest_entry['id']
    except FileNotFoundError:
        logger.error("Assistant ID file not found.")
        return None
    except (json.JSONDecodeError, KeyError) as e:
        logger.error(f"Error loading assistant ID: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"An error occurred while loading assistant ID: {str(e)}")
        return None

    return assistant_id
