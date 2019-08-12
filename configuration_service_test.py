from configuration_service import ConfigurationService
from asynctest import TestCase

class MockConfigurationService(ConfigurationService):
    def __init__(self, config_file_path, mock_config_file_contents):
        super().__init__(config_file_path)
        self.mock_config_file_contents = mock_config_file_contents

    def _read_config_file(self):
        return self.mock_config_file_contents


class BaseTestCase:
    def setUp(self):
        self.mock_config_contents = r'{ "my_prop": "my_val" }'
        self.mock_config_file_path = 'my_config.json'
        self.mock_config_service = MockConfigurationService(self.mock_config_file_path, self.mock_config_contents)

class TestGetConfigValue(BaseTestCase, TestCase):
    def setUp(self):
        BaseTestCase.setUp(self)

    def runTest(self):
        expected = "my_val"
        actual = self.mock_config_service.get("my_prop")

        assert actual == expected