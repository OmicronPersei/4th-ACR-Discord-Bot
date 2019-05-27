import sqlite3
import asynctest
from asynctest import MagicMock, call

from sql_wrapper import SQLWrapper

class MockSQLWrapper(SQLWrapper):
    def __init__(self, config, mock_sql):
        self._mock_sql = mock_sql
        super().__init__(config)

    def get_db_connection(self, db_filename):
        return self._mock_sql

class BaseSQLWrapperTests:
    def setUp(self):
        self.mock_sqlite3 = MagicMock(sqlite3)
        self.mock_sqlite3.connect = MagicMock()
        self.mock_sqlite3.execute = MagicMock()
        self.mock_sqlite3.commit = MagicMock()
        self.mock_config = { "db_filename": "forum_discord_messages.sqlite3" }

        self.sql_wrapper = MockSQLWrapper(self.mock_config, self.mock_sqlite3)

# not sure how to implement the below...
# class TestSQLWrapperChecksTableConnectsToDBSpecifiedInConfig(BaseSQLWrapperTests, asynctest.TestCase):
#     def setUp(self):
#         BaseSQLWrapperTests.setUp(self)

#     def runTest(self):
#         self.mock_sqlite3.connect.assert_called_once_with(self.mock_config["db_filename"])

class TestSQLWrapperChecksForumMessageTableExists_DoesntExist(BaseSQLWrapperTests, asynctest.TestCase):
    def setUp(self):
        BaseSQLWrapperTests.setUp(self)
        self.mock_forum_name_prefix = "xenforo1"
        self.mock_forum_id = "123"

    def sqlExecuteCreateTableSideEffect(self, *args, **kwargs):
        self.execute_calls = self.execute_calls + 1
        if self.execute_calls == 1:
            raise sqlite3.OperationalError
        elif self.execute_calls == 2:
            return MagicMock()

    def runTest(self):
        self.execute_calls = 0
        self.mock_sqlite3.execute.side_effect = self.sqlExecuteCreateTableSideEffect
        self.sql_wrapper.check_forum_has_allocated_storage(self.mock_forum_name_prefix, self.mock_forum_id)
        expected_sql = [ "select top 1 * from ForumMessageHistory",
            "create table ForumMessageHistory (forum_name_prefix nvarchar, forum_id nvarchar, thread_id nvarchar, discord_message_id nvarchar)"]
        expected_calls = [call(x) for x in expected_sql]
        self.mock_sqlite3.execute.assert_has_calls(expected_calls, any_order=False)
        self.mock_sqlite3.commit.assert_called_once()

class TestSQLWrapperChecksForumMessageTableExists_AlreadyExists(BaseSQLWrapperTests, asynctest.TestCase):
    def setUp(self):
        BaseSQLWrapperTests.setUp(self)
        self.mock_forum_name_prefix = "xenforo1"
        self.mock_forum_id = "123"

    def runTest(self):
        self.mock_sqlite3.execute.return_value = MagicMock()

        self.sql_wrapper.check_forum_has_allocated_storage(self.mock_forum_name_prefix, self.mock_forum_id)
        expected_sql = "select top 1 * from ForumMessageHistory"
        self.mock_sqlite3.execute.assert_called_with(expected_sql)



