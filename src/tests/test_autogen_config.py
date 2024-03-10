import unittest
from unittest.mock import patch
from src.autogen_configuration.autogen_config import GetConfig


class TestGetConfig(unittest.TestCase):

    def setUp(self):
        self.get_config = GetConfig()

    @patch('src.autogen_configuration.autogen_config.config_list_from_json')
    def test_load_and_enrich_config_list(self, mock_config_list_from_json):
        mock_config_list = [
            {'model': 'model1'},
            {'model': 'model2'}
        ]
        mock_config_list_from_json.return_value = mock_config_list

        expected_config_list = [
            {'model': 'model1', 'api_key': 'test_api_key'},
            {'model': 'model2', 'api_key': 'test_api_key'}
        ]

        self.get_config.api_key = 'test_api_key'
        config_list = self.get_config.load_and_enrich_config_list()

        self.assertEqual(config_list['config_list'], expected_config_list)


if __name__ == '__main__':
    unittest.main()
