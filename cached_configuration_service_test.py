from cached_configuration_service import CachedConfigurationService
from asynctest import TestCase, MagicMock, call, main

class MockCachedConfigurationService(CachedConfigurationService):
    def __init__(self, config_file_path, mock_config_file_contents):
        self._read_config_file = MagicMock(return_value=mock_config_file_contents)
        super().__init__(config_file_path)

    def _get_current_time(self):
        return self.mock_current_time

class BaseTestCase:
    def setUp(self):
        self.mock_config_contents = r'{ "config_cache_expires_after": 300, "my_prop": "my_val" }'
        self.mock_cached_config_service = MockCachedConfigurationService(None, self.mock_config_contents)

class TestConfigReadsFirstTime(BaseTestCase, TestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        self.mock_cached_config_service.mock_current_time = 1000

    def runTest(self):
        expected = "my_val"
        actual = self.mock_cached_config_service.get("my_prop")
        assert actual == expected

        expected = 300
        actual = self.mock_cached_config_service._cache_timeout_seconds
        assert actual == expected
        
        expected = 1000
        actual = self.mock_cached_config_service._cache_accessed_time
        assert actual == expected

class TestConfigReadsOnlyOnceWhileCacheIsStillFresh(BaseTestCase, TestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        

    def runTest(self):
        self.mock_cached_config_service.mock_current_time = 1000
        self.mock_cached_config_service.get("my_prop")
        self.mock_cached_config_service.mock_current_time = 1200
        self.mock_cached_config_service.get("my_prop")

        self.mock_cached_config_service._read_config_file.assert_called_once()

class TestConfigReadsMultipleTimesDueToStaleCache(BaseTestCase, TestCase):
    def setUp(self):
        BaseTestCase.setUp(self)
        

    def runTest(self):
        self.mock_cached_config_service.mock_current_time = 1000
        self.mock_cached_config_service.get("my_prop")

        # cache is now stale, should reread from disk
        self.mock_cached_config_service.mock_current_time = 1400
        self.mock_cached_config_service.get("my_prop")

        # test it was called twice, once for initial fetch, second for stale cache
        self.mock_cached_config_service._read_config_file.assert_has_calls([call(), call()])
        
# main()