from forum_thread_data_storage import ForumThreadDataStorage
import asynctest
from asynctest import MagicMock, call, TestCase

mock_forum_threads = [ {
        "forum_name": "xenforo1",
        "forum_id": "1"
    }, 
    {
        "forum_name": "xenforo1",
        "forum_id": "2"
    }]

class ForumThreadDataStorageTestBase:
    def setUp(self):
        self.mock_forum_threads = [ {
                "forum_name": "xenforo1",
                "forum_id": "1"
            }, 
            {
                "forum_name": "xenforo1",
                "forum_id": "2"
            }]
        self.mock_sql = MagicMock()
        self.mock_sql.check_forum_has_allocated_storage = MagicMock()
        self.forum_thread_data_storage = ForumThreadDataStorage(self.mock_sql)

class TestForumDataStorageChecksIfTablesExistsUponConstructionAndDoesNothingWhenExist(ForumThreadDataStorageTestBase, TestCase):
    def setUp(self):
        ForumThreadDataStorageTestBase.setUp(self)

    def runTest(self):
        self.forum_thread_data_storage.check_forums_have_allocated_storage()
        self.mock_sql.check_forum_has_allocated_storage.assert_called()

class TestForumDataStorageReturnsExistingForumThreadRecords(ForumThreadDataStorageTestBase, TestCase):
    def setUp(self):
        ForumThreadDataStorageTestBase.setUp(self)
        
        self.forum_id1_records = [
            { "forum_name": "xenforo1", "forum_id": "1", "thread_id": "1", "discord_message_id": "1" }
        ]
        self.mock_sql.get_forum_thread_records = MagicMock(return_value=self.forum_id1_records)
    
    def runTest(self):
        forum_thread_query = { "forum_name": "xenforo1", "forum_id": "1" }
        actual = self.forum_thread_data_storage.get_forum_thread_records(forum_thread_query)

        self.mock_sql.get_forum_thread_records.assert_called_once_with("xenforo1", "1")
        assert len(actual) == 1
        assert actual == self.forum_id1_records

class TestForumDataStorageStoresNewForumRecord(ForumThreadDataStorageTestBase, TestCase):
    def setUp(self):
        ForumThreadDataStorageTestBase.setUp(self)
        self.new_forum_thread_record = {
            "forum_name": "sdfadsf",
            "forum_id": "123",
            "thread_id": "q4213",
            "discord_message_id": "DSfadf"
        }

    def runTest(self):
        self.forum_thread_data_storage.store_new_forum_thread_record(self.new_forum_thread_record)

        self.mock_sql.insert_forum_thread_record.assert_called_with(self.new_forum_thread_record)

