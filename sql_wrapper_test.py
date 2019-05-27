import sqlite3
import asynctest
from asynctest import MagicMock, call

from sql_wrapper import SQLWrapper

class BaseSQLWrapperTests:
    def setUp(self):
        self.mock_sqlite3 = MagicMock(sqlite3)
        self.mock_sqlite3.connect = MagicMock()
        self.mock_config = { "db_filename": "forum_discord_messages.sqlite3" }

        self.sql_wrapper = SQLWrapper(self.mock_config, self.mock_sqlite3)

class TestSQLWrapperChecksTableConnectsToDBSpecifiedInConfig(BaseSQLWrapperTests, asynctest.TestCase):
    def setUp(self):
        BaseSQLWrapperTests.setUp(self)

    def runTest(self):
        self.mock_sqlite3.connect.assert_called_once_with(self.mock_config["db_filename"])
