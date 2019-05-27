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

class BaseSQLWrapperIntegrationTest(TestCase):
    def setUp(self):
        #Create an actual, in memory only SQLite3 database instance.
        self.db = sqlite3.connect(":memory:")
        self.sql_wrapper = MockSQLWrapper(mock_config, self.db)

class SQLWrapperIntegrationTestChecksTablesAreSetupWhenDontExist(BaseSQLWrapperIntegrationTest):
    def runTest(self):
        self.sql_wrapper.check_forum_has_allocated_storage()

        cursor = self.db.execute("select 1 from ForumMessageHistory")
        assert isinstance(cursor, sqlite3.Cursor)

class BaseSQLWrapperIntegrationTestWithTableAndData(BaseSQLWrapperIntegrationTest):
    def setUp(self):
        BaseSQLWrapperIntegrationTest.setUp(self)
        new_table_query = "create table ForumMessageHistory (forum_name nvarchar, forum_id nvarchar, thread_id nvarchar)"
        self.db.execute(new_table_query)
        insert_data = "insert into ForumMessageHistory (forum_name, forum_id, thread_id) values ('myforum', '123', '456')"
        self.db.execute(insert_data)
        self.db.commit()

class SQLWrapperIntegrationTestChecksTablesAreSetupTableAlreadyExists(BaseSQLWrapperIntegrationTestWithTableAndData):
    def runTest(self):
        self.sql_wrapper.check_forum_has_allocated_storage()

        cursor = self.db.execute("select 1 from ForumMessageHistory")
        assert isinstance(cursor, sqlite3.Cursor)

class SQLWrapperIntegrationTestGetsForumRecordsForForumId(BaseSQLWrapperIntegrationTestWithTableAndData):
    def runTest(self):
        actual = self.sql_wrapper.get_forum_thread_records("myforum", "123")
        expected_dict = {
            "forum_name": "myforum",
            "forum_id": "123",
            "thread_id": "456"
        }

        assert len(actual) == 1
        assert actual[0] == expected_dict

class SQLWrapperIntegrationTestsInsertsNewForumRecords(BaseSQLWrapperIntegrationTestWithTableAndData):
    def runTest(self):
        insert_query_dict = {
            "forum_name": "myforum",
            "forum_id": "123",
            "thread_id": "777"
        }
        self.sql_wrapper.insert_forum_thread_record(insert_query_dict)
        
        test_select_query = """
        select count(thread_id) from ForumMessageHistory
        where 1=1
        and forum_name = 'myforum'
        and forum_id = '123'
        and thread_id = '777'
        """

        c = self.db.execute(test_select_query)
        count = c.fetchone()[0]
        assert count == 1