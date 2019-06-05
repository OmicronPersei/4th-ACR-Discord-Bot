import sqlite3

from sql_wrapper import SQLWrapper
from asynctest import TestCase

class MockSQLWrapper(SQLWrapper):
    def __init__(self, config, mock_sql):
        self._mock_sql = mock_sql
        super().__init__(config)

    def _get_db_connection(self, db_filename):
        return self._mock_sql

mock_config = {
    "db_filename": None
}

class SQLWrapperIntegrationTestChecksTablesAreSetupWhenDontExist(TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.sql_wrapper = MockSQLWrapper(mock_config, self.db)

    def runTest(self):
        self.sql_wrapper.check_forum_has_allocated_storage()

        cursor = self.db.execute("select 1 from ForumMessageHistory")
        assert isinstance(cursor, sqlite3.Cursor)

class SQLWrapperIntegrationTestChecksTablesAreSetupTableAlreadyExists(TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.sql_wrapper = MockSQLWrapper(mock_config, self.db)

        new_table_query = "create table ForumMessageHistory (forum_name nvarchar, forum_id nvarchar, thread_id nvarchar)"
        self.db.execute(new_table_query)
        self.db.commit()

    def runTest(self):
        self.sql_wrapper.check_forum_has_allocated_storage()

        cursor = self.db.execute("select 1 from ForumMessageHistory")
        assert isinstance(cursor, sqlite3.Cursor)
