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
            "update_period": "60"
        }

        self.new_message_dispatcher = XenForoNewMessageDispatcher(self.mock_new_forum_detector, self.mock_discord_service, self.mock_discord_mention_service, self.mock_clock_signal, self.mock_config)



class XenForoNewMessageDispatcherTestConstructor(TestCase, Base):
    def setUp(self):
        Base.setUp(self)

    def runTest(self):
        self.mock_clock_signal.create_callback.assert_called_with("60", self.new_message_dispatcher._check_for_new_threads)
    
