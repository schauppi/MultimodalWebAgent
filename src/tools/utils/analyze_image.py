from src.configs.logging.logging_config import setup_logging
from src.tools.utils.openai_client import get_openai_client

import logging

setup_logging()
logger = logging.getLogger()


def analyze_image(message_history, **kwargs):
    """
    Analyzes an image using OpenAI's GPT-4 Vision model and returns the response message.

    Args:
        message_history (list): A list of message objects representing the conversation history.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        str: The response message if successful, else logs error and returns an error message.
    """

    try:
        logger.info("Getting OpenAI client.")
        client = get_openai_client()

        logger.info("Sending request to OpenAI's GPT-4 Vision model.")
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=message_history,
            max_tokens=1024,
            temperature=0.1,
            **kwargs)

        message = response.choices[0].message
        message_text = message.content

        logger.info("Image analysis completed successfully.")
        return message_text

    except Exception as e:
        logger.error(
            "Failed to analyze image with OpenAI's GPT-4 Vision model.", exc_info=True)
        return "An error occurred while analyzing the image. Please try again later."
