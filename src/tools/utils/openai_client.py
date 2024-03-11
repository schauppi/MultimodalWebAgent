from src.configs.logging.logging_config import setup_logging
import openai
from dotenv import load_dotenv
import threading
import instructor
import os
import logging

setup_logging()
logger = logging.getLogger()

dotenv_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), '..', '..', '..', '.env'))

load_dotenv(dotenv_path)

client_lock = threading.Lock()
client = None


def get_openai_client():
    """
    Returns an OpenAI client instance.

    Args:
        None

    Returns:
        openai.OpenAI: An OpenAI client instance.
    """
    global client
    with client_lock:
        if client is None:
            try:
                logging.info("Creating OpenAI client")
                api_key = openai.api_key or os.getenv('OPENAI_API_KEY')
                if api_key is None:
                    raise ValueError(
                        "OpenAI API key is not set. Please set it using set_openai_key.")
                client = instructor.patch(openai.OpenAI(api_key=api_key,
                                                        max_retries=5,))
                logging.info("OpenAI client created successfully.")
            except Exception as e:
                logging.error(f"Error creating OpenAI client: {str(e)}")
    return client
