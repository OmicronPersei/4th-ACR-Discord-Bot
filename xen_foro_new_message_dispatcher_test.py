from asynctest import TestCase, MagicMock
from asyncio import Future
from xen_foro_new_message_dispatcher import XenForoNewMessageDispatcher

class Base:
    def setUp(self):
        self.mock_new_forum_detector = MagicMock()
        self.mock_discord_service = MagicMock()
        self.mock_discord_mention_service = MagicMock()
        self.mock_forum_url_thread_factory = MagicMock()
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

        self.new_message_dispatcher = XenForoNewMessageDispatcher(self.mock_new_forum_detector, self.mock_discord_service, self.mock_discord_mention_service, self.mock_clock_signal, self.mock_forum_url_thread_factory, self.mock_config)

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
        self.url = "generated url"
        self.mock_forum_url_thread_factory.get_url=MagicMock(return_value=self.url)
        self.mock_new_forum_detector.get_threads_needing_messages = MagicMock(return_value = self.new_forum_threads)
        self.mention_service_return_val = "mention service did work"
        self.mock_discord_mention_service.perform_replacement = MagicMock(return_value=self.mention_service_return_val)

        self.mock_discord_service.send_channel_message = MagicMock(return_value=Future())
        self.mock_discord_service.send_channel_message.return_value.set_result(None)

    async def runTest(self):
        await self.new_message_dispatcher._check_for_new_threads()

        self.mock_new_forum_detector.get_threads_needing_messages.assert_called()

        self.mock_forum_url_thread_factory.get_url.assert_called_with("https://myforum.xyz/", "111", "123")

        expected_template = "A new forum post has appeared! {}".format(self.url)
        self.mock_discord_mention_service.perform_replacement.assert_called_with(expected_template)

        self.mock_discord_service.send_channel_message.assert_called_with(self.mention_service_return_val, "forum posts")
    
