from src.utils.logging.log_config import setup_logging
import json
import logging

setup_logging()

logger = logging.getLogger(__name__)


class ToolDefinitionFactory:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

    def load_config(self, path):
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

    def create_tool_definition(self, tool_type):
        tool_config = self.config.get(tool_type)
        if not tool_config:
            logger.error(f"No tool definition found for type: {tool_type}")
            raise ValueError(f"No tool definition found for type: {tool_type}")

        try:
            return {
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
