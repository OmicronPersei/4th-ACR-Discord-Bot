import sqlite3
from asynctest import MagicMock, call, TestCase

from forum_watcher.sql_wrapper import SQLWrapper

class MockSQLWrapper(SQLWrapper):
    def __init__(self, config, mock_sql):
        self._mock_sql = mock_sql
        super().__init__(config)

    def _get_db_connection(self, db_filename):
        return self._mock_sql

class BaseSQLWrapperTests:
    def setUp(self):
        self.mock_sqlite3 = MagicMock(sqlite3)
        self.mock_sqlite3.connect = MagicMock()
        self.mock_sqlite3.execute = MagicMock()
        self.mock_sqlite3.commit = MagicMock()
        self.mock_config = { "db_filename": "forum_discord_messages.sqlite3" }

        self.sql_wrapper = MockSQLWrapper(self.mock_config, self.mock_sqlite3)

class TestSQLWrapperChecksForumMessageTableExists_DoesntExist(BaseSQLWrapperTests, TestCase):
    def setUp(self):
        BaseSQLWrapperTests.setUp(self)
        self.mock_forum_name = "xenforo1"
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
        self.sql_wrapper.check_forum_has_allocated_storage()
        expected_sql = [ "select 1 from ForumMessageHistory",
            "create table ForumMessageHistory (forum_name nvarchar, forum_id nvarchar, thread_id nvarchar)"]
        expected_calls = [call(x) for x in expected_sql]
        self.mock_sqlite3.execute.assert_has_calls(expected_calls, any_order=False)
        self.mock_sqlite3.commit.assert_called_once()

class TestSQLWrapperChecksForumMessageTableExists_AlreadyExists(BaseSQLWrapperTests, TestCase):
    def setUp(self):
        BaseSQLWrapperTests.setUp(self)
        self.mock_forum_name = "xenforo1"
        self.mock_forum_id = "123"

    def runTest(self):
        self.mock_sqlite3.execute.return_value = MagicMock()

        self.sql_wrapper.check_forum_has_allocated_storage()
        expected_sql = "select 1 from ForumMessageHistory"
        self.mock_sqlite3.execute.assert_called_with(expected_sql)


class TestSQLWrapperReturnsRecords(BaseSQLWrapperTests, TestCase):
    def setUp(self):
        BaseSQLWrapperTests.setUp(self)
        self.mock_forum_name = "xenforo1"
        self.mock_forum_id = "123"
        self.mock_sqlite3.execute.return_value = iter([
                (self.mock_forum_name, self.mock_forum_id, "456"),
                (self.mock_forum_name, self.mock_forum_id, "457"),
            ])
        
    def runTest(self):
        actual = self.sql_wrapper.get_forum_thread_records(self.mock_forum_name, self.mock_forum_id)

        expected_sql_query = "select * from ForumMessageHistory where forum_name='{}' and forum_id='{}'".format(self.mock_forum_name, self.mock_forum_id)
        self.mock_sqlite3.execute.assert_called_once_with(expected_sql_query)
        
        assert len(actual) == 2

        assert actual[0]["forum_name"] == self.mock_forum_name
        assert actual[0]["forum_id"] == self.mock_forum_id
        assert actual[0]["thread_id"] == "456"

        assert actual[1]["forum_name"] == self.mock_forum_name
        assert actual[1]["forum_id"] == self.mock_forum_id
        assert actual[1]["thread_id"] == "457"


class TestSQLWrapperInsertsRecords(BaseSQLWrapperTests, TestCase):
    def setUp(self):
        BaseSQLWrapperTests.setUp(self)
        self.mock_record = {
            "forum_name": "my_forum",
            "forum_id": "123",
            "thread_id": "789"
        }
    
    def runTest(self):
        expected_sql_insert = """insert into ForumMessageHistory (forum_name, forum_id, thread_id)
        values ('{}', '{}', '{}')""".format(
            "my_forum",
            "123",
            "789"
        )

        self.sql_wrapper.insert_forum_thread_record(self.mock_record)

        self.mock_sqlite3.execute.assert_called_with(expected_sql_insert)
        self.mock_sqlite3.commit.assert_called()