from configuration_service import ConfigurationService

cache_expire_key = "config_cache_expires_after"

class CachedConfigurationService(ConfigurationService):
    def __init__(self, config_file_path):
        super().__init__(config_file_path)
        self._cache_timeout_seconds = self.get_config_value(cache_expire_key)