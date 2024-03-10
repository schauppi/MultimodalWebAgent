import unittest
from unittest.mock import patch, mock_open
import os
import logging.config
# Assuming your updated code is in a file named log_config.py
from src.configs.logging.logging_config import setup_logging


class TestSetupLogging(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"version": 1}')
    @patch('logging.config.dictConfig')
    def test_default_path(self, mock_dict_config, mock_file, mock_exists):
        setup_logging()
        mock_exists.assert_called_once_with(
            'src/configs/logging/logging_config.json')
        mock_file.assert_called_once_with(
            'src/configs/logging/logging_config.json', 'rt')
        mock_dict_config.assert_called_once()

    @patch('os.path.exists', return_value=False)
    @patch('logging.basicConfig')
    def test_fallback_to_basic_config(self, mock_basic_config, mock_exists):
        setup_logging()
        mock_exists.assert_called_once_with(
            'src/configs/logging/logging_config.json')
        mock_basic_config.assert_called_once_with(level=logging.INFO)


if __name__ == '__main__':
    unittest.main()
