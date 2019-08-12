from configuration_service import ConfigurationService
import time

cache_expire_key = "config_cache_expires_after"

class CachedConfigurationService(ConfigurationService):
    def __init__(self, config_file_path):
        self._cache_accessed_time = None
        self._cached_config = None
        self._cache_timeout_seconds = None

        super().__init__(config_file_path)
        
    def _get_config_contents(self):
        if self._is_cache_stale():
            self.load_config_and_set_cache()

        return self._cached_config

    def _is_cache_stale(self):
        if (not self._cache_accessed_time) or (not self._cache_timeout_seconds):
            return True

        cache_expires_time = (self._cache_accessed_time + self._cache_timeout_seconds)
        current_time = self._get_current_time()
        return current_time >= cache_expires_time

    def load_config_and_set_cache(self):
        self._cached_config = ConfigurationService._get_config_contents(self)
        
        self._cache_accessed_time = self._get_current_time()
        self._cache_timeout_seconds = self._cached_config[cache_expire_key]
    
    def _get_current_time(self):
        return time.time()