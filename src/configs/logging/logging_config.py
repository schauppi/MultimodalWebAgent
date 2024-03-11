import json
import os
import logging.config
from typing import Optional

from src.configs.logging.color_formatter import ColoredFormatter


def setup_logging(default_path: str = 'src/configs/logging/logging_config.json', default_level: int = logging.INFO) -> None:
    """
    Setup logging configuration.

    Args:
        default_path (str): The default path to the logging configuration file.
        default_level (int): The default logging level.

    Returns:
        None
    """
    path = default_path
    try:
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)

            logging.config.dictConfig(config)

            for _, handler_details in config['handlers'].items():
                if 'formatter' in handler_details:
                    formatter_config = config['formatters'][handler_details['formatter']]
                    formatter = ColoredFormatter(
                        fmt=formatter_config['format'])
                    logging.getLogger().handlers[0].setFormatter(formatter)
        else:
            logging.basicConfig(level=default_level)
    except Exception as e:
        print(f"Error occurred while setting up logging: {e}")
