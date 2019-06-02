from asynctest import TestCase, MagicMock
from xen_foro_new_message_dispatcher import XenForoNewMessageDispatcher

class Base:
    def setUp(self):
        self.mock_new_forum_detector = MagicMock()
        self.mock_discord_service = MagicMock()
        self.mock_discord_mention_service = MagicMock()
        self.mock_clock_signal = MagicMock()
        self.mock_clock_signal.create_callback = MagicMock()
        self.mock_config = {
            "update_period": "60",
            "base_url": "https://myforum.xyz/",
            "forums": [{
                    "forum_id": "111",
                    "target_discord_channel": "forum posts",
                    "message_template": "A new forum post has appeared! {thread_url}",
                    "discord_message_emojis": []
                }]
        }

        self.new_message_dispatcher = XenForoNewMessageDispatcher(self.mock_new_forum_detector, self.mock_discord_service, self.mock_discord_mention_service, self.mock_clock_signal, self.mock_config)

class XenForoNewMessageDispatcherTestConstructor(TestCase, Base):
    def setUp(self):
        Base.setUp(self)

    def runTest(self):
        self.mock_clock_signal.create_callback.assert_called_with("60", self.new_message_dispatcher._check_for_new_threads)

class XenForoNewMessageDispatcherHandlesNewlyDetectedForumPost(TestCase, Base):
    def setUp(self):
        Base.setUp(self)

        self.new_forum_threads = [{
            "forum_id": "111",
            "thread_id": "123"
        }]
        self.mock_new_forum_detector.get_threads_needing_messages = MagicMock(return_value = self.new_forum_threads)
        
        self.
    
