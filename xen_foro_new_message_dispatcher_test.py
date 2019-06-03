from asynctest import TestCase, MagicMock
from asyncio import Future
from xen_foro_new_message_dispatcher import XenForoNewMessageDispatcher

class MockXenForoNewMessageDispatcher(XenForoNewMessageDispatcher):
    def __init__(self, xen_foro_new_thread_detector, discord_service, discord_mention_factory, forum_thread_data_storage, forum_thread_url_factory, config, mock_clock_source):
        self.mock_clock_source = mock_clock_source
        super().__init__(xen_foro_new_thread_detector, discord_service, discord_mention_factory, forum_thread_data_storage, forum_thread_url_factory, config)

    def _get_clock_source(self, update_period):
        self.mock_update_period = update_period
        return self.mock_clock_source

class TestBase:
    def setUp(self):
        self.mock_new_forum_detector = MagicMock()
        self.mock_discord_service = MagicMock()
        self.mock_discord_mention_factory = MagicMock()
        self.mock_forum_url_thread_factory = MagicMock()
        self.mock_forum_thread_data_storage = MagicMock()
        self.mock_config = {
            "forum_name": "my_forum",
            "update_period": "60",
            "base_url": "https://myforum.xyz/",
            "forums": [{
                    "forum_id": "111",
                    "target_discord_channel": "forum posts",
                    "message_template": "A new forum post has appeared! {thread_url}",
                    "discord_message_emojis": []
                }]
        }

        self.mock_clock_signal = MagicMock()
        self.mock_clock_signal.callbacks = []
        self.mock_clock_signal.start = MagicMock()
        self.mock_clock_signal.stop = MagicMock()

        self.new_message_dispatcher = MockXenForoNewMessageDispatcher(self.mock_new_forum_detector, self.mock_discord_service, self.mock_discord_mention_factory, self.mock_forum_thread_data_storage, self.mock_forum_url_thread_factory, self.mock_config, self.mock_clock_signal)

class XenForoNewMessageDispatcherTestConstructor(TestCase, TestBase):
    def setUp(self):
        TestBase.setUp(self)

    def runTest(self):
        assert len(self.new_message_dispatcher.mock_clock_source.callbacks) == 1
        assert callable(self.new_message_dispatcher.mock_clock_source.callbacks[0])
        assert int(self.new_message_dispatcher.mock_update_period) == 60

class XenForoNewMessageDispatcherTestStart(TestCase, TestBase):
    def setUp(self):
        TestBase.setUp(self)

    def runTest(self):
        self.new_message_dispatcher.start()

        self.mock_clock_signal.start.assert_called()

class XenForoNewMessageDispatcherTestStop(TestCase, TestBase):
    def setUp(self):
        TestBase.setUp(self)

    def runTest(self):
        self.new_message_dispatcher.stop()

        self.mock_clock_signal.stop.assert_called()

class XenForoNewMessageDispatcherHandlesNewlyDetectedForumPost(TestCase, TestBase):
    def setUp(self):
        TestBase.setUp(self)

        self.new_forum_threads = [{
            "forum_id": "111",
            "thread_id": "123"
        }]
        self.url_from_factory = "generated url"
        self.mock_forum_url_thread_factory.get_url=MagicMock(return_value=self.url_from_factory)
        self.mock_new_forum_detector.get_threads_needing_messages = MagicMock(return_value = self.new_forum_threads)
        self.mention_service_return_val = "mention service did work"
        self.mock_discord_mention_factory.perform_replacement = MagicMock(return_value=self.mention_service_return_val)

        self.mock_discord_service.send_channel_message = MagicMock(return_value=Future())
        self.mock_discord_service.send_channel_message.return_value.set_result(None)

        self.mock_forum_thread_data_storage.store_new_forum_thread_record = MagicMock()

    async def runTest(self):
        callback = self.mock_clock_signal.callbacks[0]
        await callback()

        self.mock_new_forum_detector.get_threads_needing_messages.assert_called()

        self.mock_forum_url_thread_factory.get_url.assert_called_with("https://myforum.xyz/", "111", "123")

        expected_template = "A new forum post has appeared! {}".format(self.url_from_factory)
        self.mock_discord_mention_factory.perform_replacement.assert_called_with(expected_template)

        self.mock_discord_service.send_channel_message.assert_called_with(self.mention_service_return_val, "forum posts")

        expected_new_forum_thread_record = {
            "forum_name": "my_forum",
            "forum_id": "111",
            "thread_id": "123"
        }
        self.mock_forum_thread_data_storage.store_new_forum_thread_record.assert_called_with(expected_new_forum_thread_record)

    
