from announcement_service import AnnouncementService
from discord_service import DiscordService
from asynctest import TestCase, MagicMock, Mock
from asyncio import Future

from test_utils import MockConfigurationService, create_mock_message

class TestMakeAnnouncement(TestCase):
    def setUp(self):
        mock_config_obj = {
            "announcement_service": {
                "command_keyword": "!announce"
            }
        }

        self.mock_config = MockConfigurationService(mock_config_obj)

        self.mock_discord_service = Mock(DiscordService)

        self.announcement_service = AnnouncementService(self.mock_config, self.mock_discord_service)

    async def runTest(self):
        mock_message = create_mock_message("!announce operations This is an operation announcement", "the chan")
        await self.announcement_service.bot_command_callback(mock_message)

        self.mock_discord_service.send_channel_message.assert_called_with("This is an operation announcement", "operations")
