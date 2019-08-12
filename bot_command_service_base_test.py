from bot_command_service_base import BotCommandServiceBase
from asynctest import MagicMock, TestCase

from test_utils import MockConfigurationService

class TestSetsUpCallbackWithDiscordService(TestCase):
    def setUp(self):
        self.mock_config = MockConfigurationService({ "my_service": { "command_keyword": "!roles" } })
        self.mock_discord_service = MagicMock()
        self.mock_discord_service.create_listener_for_bot_command = MagicMock()

    def runTest(self):
        bot_command_service = BotCommandServiceBase(self.mock_config, "my_service", self.mock_discord_service)

        self.mock_discord_service.create_listener_for_bot_command.assert_called_with("!roles", bot_command_service.bot_command_callback)


