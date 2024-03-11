from src.configs.logging.logging_config import setup_logging

import logging

setup_logging()
logger = logging.getLogger()


def get_vision_template(context: str, screenshot: str, question: str) -> list:
    """
    Returns a message chat template for the vision model.

    Args:
        context (str): The context of the message chat.
        screenshot (str): A base64 encoded string representing the screenshot of the current web page.
        question (str): The user's query string.

    Returns:
        list: A list of dictionaries representing the message chat template for the vision model.
    """

    try:
        logger.info("Creating vision template")
        message_chat = [
            {
                "role": "system",
                "content": context,
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{screenshot}",
                    },
                    {
                        "type": "text",
                        "text": f"{question}",
                    }
                ]
            }
        ]
        return message_chat
    except Exception as e:
        logger.error(f"Error occurred in get_vision_template: {e}")
        return []
