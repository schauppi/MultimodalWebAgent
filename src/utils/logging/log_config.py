import logging.config
import json
import os
from typing import Optional

import logging.config


def setup_logging(default_path: str = 'logging_config.json', default_level: int = logging.INFO, env_key: str = 'LOG_CFG') -> None:
    """Setup logging configuration"""
    path: str = default_path
    value: Optional[str] = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config: dict = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
