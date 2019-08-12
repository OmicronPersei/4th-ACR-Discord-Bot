from cached_configuration_service import CachedConfigurationService
from asynctest import TestCase, MagicMock

class MockCachedConfigurationService(CachedConfigurationService):
    def __init__(self, config_file_path, mock_config_file_contents):
        self._get_config_contents = MagicMock(return_value=mock_config_file_contents)
        super().__init__(config_file_path)

class BaseTestCase:
    def setUp(self):
        self.mock_config_contents = { "config_cache_expires_after": 300, "my_prop": "my_val" }
        self.mock_cached_config_service = MockCachedConfigurationService(None, self.mock_config_contents)

class TestReadsConfigAndRecordsFirstAccessTime(BaseTestCase, TestCase):
    def setUp(self):
        BaseTestCase.setUp(self)

    def runTest(self):
        expected = 300
        actual = self.mock_cached_config_service._cache_timeout_seconds
        assert actual == expected
        
        expected = "my_val"
        actual = self.mock_cached_config_service.get_config_value("my_prop")
        assert actual == expected

        