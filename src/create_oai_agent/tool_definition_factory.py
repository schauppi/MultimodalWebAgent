from src.configs.logging.logging_config import setup_logging
import json
import logging

setup_logging()

logger = logging.getLogger(__name__)


class ToolDefinitionFactory:
    """
    Factory class for creating tool definitions.

    Methods:
        load_config(path: str) -> dict:
            Load the configuration data from the configuration file.
        create_tool_definition(tool_type: str) -> dict:
            Create a tool definition based on the tool type.
    """

    def __init__(self, config_path: str) -> None:
        """
        Initialize the factory with the path to the configuration file.

        Args:
            config_path (str): The path to the configuration file.
        """
        self.config = self.load_config(config_path)

    def load_config(self, path: str) -> dict:
        """
        Load the configuration data from the configuration file.

        Args:
            path (str): The path to the configuration file.

        Returns:
            dict: The loaded configuration data.
        """
        try:
            with open(path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logger.error(f"Config file not found at path: {path}")
            raise
        except json.JSONDecodeError:
            logger.error(
                f"Failed to parse JSON from config file at path: {path}")
            raise

    def create_tool_definition(self, tool_type: str) -> dict:
        """
        Create a tool definition based on the tool type.

        Args:
            tool_type (str): The type of the tool.

        Returns:
            dict: The tool definition.
        """
        tool_config = self.config.get(tool_type)
        if not tool_config:
            logger.error(f"No tool definition found for type: {tool_type}")
            raise ValueError(f"No tool definition found for type: {tool_type}")

        try:
            return {
                "type": 'function',
                "function": {
                    "name": tool_config['name'],
                    "description": tool_config['description'],
                    "parameters": {
                        "properties": tool_config['parameters'],
                        "required": tool_config['required'],
                        "type": "object"
                    }
                }
            }
        except KeyError as e:
            logger.error(
                f"Key {e} not found in tool config for type: {tool_type}")
            raise
