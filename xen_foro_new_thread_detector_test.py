from asynctest import TestCase, MagicMock, main
from xen_foro_new_thread_detector import XenForoNewThreadDetector

mock_config = {
    "forum_name": "my_forum",
    "base_url": "http://forum",
    "forums": [ {
        "update_period": "60",
        "forum_id": "123",
        "target_discord_channel": "forum posts",
        "message_template": "A new forum post has appeared! {thread_url}",
        "discord_message_emojis": []
    }]
}
mock_token = "asdfs"

class TestThreadProcessorReturnsNoMessagesToSend(TestCase):
    def setUp(self):
        self.thread_getter = MagicMock()
        self.threads_from_forum = [{
            "thread_id": "111",
            "first_message_contents": "post here"
        }]
        self.thread_getter.get_threads = MagicMock(return_value = self.threads_from_forum)

        self.threads_from_data_storage = [{
            "thread_id": "111",
            "first_message_contents": "post here"
        }]
        self.thread_data_storage = MagicMock()
        self.thread_data_storage.get_forum_thread_records = MagicMock(return_value=self.threads_from_data_storage)

        self.thread_processor = XenForoNewThreadDetector(self.thread_getter, self.thread_data_storage, mock_config, mock_token)

    def runTest(self):
        actual = self.thread_processor.get_threads_needing_messages()

        assert len(actual) == 0
        self.thread_getter.get_threads.assert_called_with("http://forum", "asdfs", "123")
        self.thread_data_storage.get_forum_thread_records.assert_called_with({"forum_name": "my_forum", "forum_id": "123"})

class TestThreadProcessorReturnsOneMessageToSend(TestCase):
    def setUp(self):
        self.thread_getter = MagicMock()
        self.threads_from_forum = [{
            "thread_id": "111",
            "first_message_contents": "post here"
        },
        {
            "thread_id": "222",
            "first_message_contents": "new and improved post, last one sucked really"
        }]
        self.thread_getter.get_threads = MagicMock(return_value = self.threads_from_forum)

        self.threads_from_data_storage = [{
            "thread_id": "111",
            "first_message_contents": "post here"
        }]
        self.thread_data_storage = MagicMock()
        self.thread_data_storage.get_forum_thread_records = MagicMock(return_value=self.threads_from_data_storage)

        self.thread_processor = XenForoNewThreadDetector(self.thread_getter, self.thread_data_storage, mock_config, mock_token)

    def runTest(self):
        actual = self.thread_processor.get_threads_needing_messages()

        assert len(actual) == 1
        assert actual[0] == {
            "thread_id": "222",
            "first_message_contents": "new and improved post, last one sucked really"
        }
        self.thread_getter.get_threads.assert_called_with("http://forum", "asdfs", "123")
        self.thread_data_storage.get_forum_thread_records.assert_called_with({"forum_name": "my_forum", "forum_id": "123"})

class TestThreadProcessorReturnsTwoMessagesToSendWhenNoPreviousRecorded(TestCase):
    def setUp(self):
        self.thread_getter = MagicMock()
        self.threads_from_forum = [{
            "thread_id": "111",
            "first_message_contents": "post here"
        },
        {
            "thread_id": "222",
            "first_message_contents": "new and improved post, last one sucked really"
        }]
        self.thread_getter.get_threads = MagicMock(return_value = self.threads_from_forum)

        self.threads_from_data_storage = []
        self.thread_data_storage = MagicMock()
        self.thread_data_storage.get_forum_thread_records = MagicMock(return_value=self.threads_from_data_storage)

        self.thread_processor = XenForoNewThreadDetector(self.thread_getter, self.thread_data_storage, mock_config, mock_token)

    def runTest(self):
        actual = self.thread_processor.get_threads_needing_messages()

        assert len(actual) == 2
        assert actual[0] == {
            "thread_id": "111",
            "first_message_contents": "post here"
        }
        assert actual[1] == {
            "thread_id": "222",
            "first_message_contents": "new and improved post, last one sucked really"
        }
        self.thread_getter.get_threads.assert_called_with("http://forum", "asdfs", "123")
        self.thread_data_storage.get_forum_thread_records.assert_called_with({"forum_name": "my_forum", "forum_id": "123"})        

        
class TestThreadDetectorChecksStorageUponInstantiation(TestCase):
    def setUp(self):
        self.thread_getter = MagicMock()
        self.thread_data_storage = MagicMock()
        self.thread_data_storage.check_forums_have_allocated_storage = MagicMock()

    def runTest(self):
        self.thread_processor = XenForoNewThreadDetector(self.thread_getter, self.thread_data_storage, mock_config, mock_token)

        self.thread_data_storage.check_forums_have_allocated_storage.assert_called()