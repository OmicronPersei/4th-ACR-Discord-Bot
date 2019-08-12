from cached_configuration_service import CachedConfigurationService
from asynctest import TestCase, MagicMock, main

class MockCachedConfigurationService(CachedConfigurationService):
    def __init__(self, config_file_path, mock_config_file_contents):
        self._read_config_file = MagicMock(return_value=mock_config_file_contents)
        super().__init__(config_file_path)

    def _get_current_time(self):
        return self.mock_current_time()

class BaseTestCase:
    def setUp(self):
        self.mock_config_contents = r'{ "config_cache_expires_after": 300, "my_prop": "my_val" }'
        self.mock_cached_config_service = MockCachedConfigurationService(None, self.mock_config_contents)

class TestConfigReadsFirstTime(BaseTestCase, TestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.mock_cached_config_service.mock_current_time = MagicMock(return_value=1000)

    def runTest(self):
        expected = "my_val"
        actual = self.mock_cached_config_service.get_config_value("my_prop")
        assert actual == expected

        expected = 300
        actual = self.mock_cached_config_service._cache_timeout_seconds
        assert actual == expected
        
        expected = 1000
        actual = self.mock_cached_config_service._cache_accessed_time
        assert actual == expected

# main()