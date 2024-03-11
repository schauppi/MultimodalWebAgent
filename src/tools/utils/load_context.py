from src.configs.logging.logging_config import setup_logging

import logging
import json

setup_logging()
logger = logging.getLogger()


def load_context(prompt_template: str) -> str:
    """
    Load the prompt for the assistant from the specified JSON file.

    Args:
        None

    Returns:
        str: The prompt for the assistant to use in generating responses.
    """
    try:
        logger.info("Loading the prompt from the JSON file.")
        with open('src/tools/utils/prompts.json', 'r') as file:
            prompt = json.load(file)
            prompt = prompt[prompt_template]["prompt"]
            return prompt
    except Exception as e:
        logger.error(
            "Failed to load the prompt from the JSON file.", exc_info=True)
        raise
