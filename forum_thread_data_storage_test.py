from forum_thread_data_storage import ForumThreadDataStorage
import asynctest
from asynctest import MagicMock, call

mock_forum_threads = [ {
        "forum_name_prefix": "xenforo1",
        "forum_id": "1"
    }, 
    {
        "forum_name_prefix": "xenforo1",
        "forum_id": "2"
    }]

class ForumThreadDataStorageTestBase:
    def setUp(self):
        self.mock_forum_threads = [ {
                "forum_name_prefix": "xenforo1",
                "forum_id": "1"
            }, 
            {
                "forum_name_prefix": "xenforo1",
                "forum_id": "2"
            }]
        self.mock_sql = MagicMock()
        self.mock_sql.check_forum_has_allocated_storage = MagicMock()
        self.forum_thread_data_storage = ForumThreadDataStorage(self.mock_sql, mock_forum_threads)

class TestForumDataStorageChecksIfTablesExistsUponConstructionAndDoesNothingWhenExist(ForumThreadDataStorageTestBase, asynctest.TestCase):
    def setUp(self):
        ForumThreadDataStorageTestBase.setUp(self)

    def runTest(self):
        expected_calls = [call("xenforo1", "1"), call("xenforo1", "2")]
        self.mock_sql.check_forum_has_allocated_storage.assert_has_calls(expected_calls, any_order=True)

class TestForumDataStorageReturnsExistingForumThreadRecords(ForumThreadDataStorageTestBase, asynctest.TestCase):
    def setUp(self):
        ForumThreadDataStorageTestBase.setUp(self)
        
        self.forum_id1_records = [
            { "forum_name_prefix": "xenforo1", "forum_id": "1", "thread_id": "1", "discord_message_id": "1" }
        ]
        self.mock_sql.get_forum_records = MagicMock(return_value=self.forum_id1_records)
    
    def runTest(self):
        forum_thread_query = { "forum_name_prefix": "xenforo1", "forum_id": "1" }
        actual = self.forum_thread_data_storage.get_forum_thread_records(forum_thread_query)

        self.mock_sql.get_forum_records.assert_called_once_with("xenforo1", "1")
        assert len(actual) == 1
        assert actual == self.forum_id1_records
    


        


