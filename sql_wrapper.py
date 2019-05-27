class SQLWrapper:
    def __init__(self, config, sql_lite_instance):
        self._sqlite3_instance = sql_lite_instance
        self._config = config

        self.connect()

    def connect(self):
        db_filename = self._config["db_filename"]
        self._sqlite3_instance.connect(db_filename)