from src.configs.logging.logging_config import setup_logging
import autogen
from autogen import config_list_from_json
import logging
from dotenv import load_dotenv

import os

setup_logging()

logger = logging.getLogger(__name__)

dotenv_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), '..', '..', '.env'))

try:
    load_dotenv(dotenv_path=dotenv_path)
    logger.info("Environment variables loaded successfully.")
except Exception as e:
    logger.error("Failed to load the .env file.", exc_info=e)


class GetConfig:
    """
    Get and enrich config from config file.

    Methods:
        __init__():
            Initialize with API key and config list.
        base_dir() -> str:
            Returns the base directory path.
        load_and_enrich_config_list() -> dict:
            Loads config list from a JSON file and enriches it with the API key.

    """

    def __init__(self) -> None:
        """
        Initialize with API key and config list.

        Args:
            None
        """
        logger.info('Initializing GetConfig class')
        self.api_key = os.environ.get('OPENAI_API_KEY', '')
        if not self.api_key:
            logger.error('OPENAI_API_KEY not found in environment variables')
        self.config_list = self.load_and_enrich_config_list()

    @property
    def base_dir(self) -> str:
        """
        Returns the base directory path.

        Args:
            None

        Returns:
            str: The base directory path.
        """
        base_dir = os.path.dirname(os.path.dirname(__file__))
        logger.info(f'Retrieved base directory path: {base_dir}')
        return base_dir

    def load_and_enrich_config_list(self) -> dict:
        """
        Loads config list from a JSON file and enriches it with the API key.

        Args:
            None

        Returns:
            dict: The enriched config list.
        """
        config_path = 'src/autogen_configuration/utils/oai_config_list.json'
        try:
            config_list = config_list_from_json(
                env_or_file=config_path,
                filter_dict={"model": os.environ.get('OPENAI_MODEL', '')}
            )
            logger.info('Config list loaded successfully')
            for config in config_list:
                config['api_key'] = self.api_key
            logger.info('Config list enriched with API key')
        except Exception as e:
            logger.error(
                "Failed to load or enrich the config list.", exc_info=e)
            config_list = []
        return {'config_list': config_list}


# test
config = GetConfig()
