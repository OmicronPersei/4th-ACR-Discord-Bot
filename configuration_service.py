import json

class ConfigurationService:

    def __init__(self, config_file_path):
        self._config_file_path = config_file_path

    def get(self, prop_name):
        config = self._get_config_contents()
        return config[prop_name]

    def _get_config_contents(self):
        file_contents = self._read_config_file()
        return json.loads(file_contents)

    def _read_config_file(self):
        with open(self._config_file_path, mode='r') as f:
            return f.read()