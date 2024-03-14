from src.configs.logging.logging_config import setup_logging
from src.create_oai_agent.oai_agent_creator import OAIAssistantCreator

import logging
import os

setup_logging()
logger = logging.getLogger()


def create_agent(assistant_type: str):
    """
    Create an OpenAI assistant with the specified tools and instructions.

    Args:
        assistant_type (str): The type of assistant to create.

    Returns:
        None
    """
    try:
        dotenv_path = os.path.normpath(os.path.join(
            os.path.dirname(__file__), '..', '..', '.env'))
        config_path = 'src/create_oai_agent/utils/tool_definitions.json'
        instruction_path = 'src/create_oai_agent/utils/oai_instructions.json'
        assistant_save_path = "src/data/assistant_id.json"
        logger.info("Creating OpenAI Assistant...")
        creator = OAIAssistantCreator(
            dotenv_path, config_path, instruction_path, assistant_save_path, assistant_type)
        creator.run()
    except Exception as e:
        logger.error(f"An error occurred while creating the agent: {str(e)}")
