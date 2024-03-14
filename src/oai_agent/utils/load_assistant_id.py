from src.configs.logging.logging_config import setup_logging

import logging
import json
import datetime

setup_logging()
logger = logging.getLogger()


def load_assistant_id(assistant_type: str) -> str:
    """
    Load the assistant ID from the assistant ID file.

    Args:
    - assistant_type (str): The type of assistant to load.

    Returns:
    - assistant_id (str): The assistant ID. 
    """
    try:
        with open("src/data/assistant_id.json", "r") as file:
            data = json.load(file)
            filtered_data = [
                entry for entry in data if entry['type'] == assistant_type]
            latest_entry = max(filtered_data, key=lambda x: datetime.datetime.strptime(
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
