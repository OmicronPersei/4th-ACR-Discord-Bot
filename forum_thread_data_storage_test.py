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

class TestForumDataStorageChecksIfTablesExistsUponConstructionAndDoesNothingWhenExist(asynctest.TestCase):
    def setUp(self):
        self.mock_sql = MagicMock()
        self.mock_sql.check_forum_has_allocated_storage = MagicMock()
        self.forum_thread_data_storage = ForumThreadDataStorage(self.mock_sql, mock_forum_threads)

    def runTest(self):
        expected_calls = [call("xenforo1", "1"), call("xenforo1", "2")]
        self.mock_sql.check_forum_has_allocated_storage.assert_has_calls(expected_calls, any_order=True)
        


