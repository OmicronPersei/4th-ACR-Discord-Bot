from announcement_service import AnnouncementService, service_name
from discord_service import DiscordService
from asynctest import TestCase, MagicMock, Mock, main
from asyncio import Future

from test_utils import MockConfigurationService, create_mock_message, create_mock_role, create_mock_reaction

class TestAnnouncementBase:
    def setUp(self):
        mock_config_obj = {
            service_name: {
                "command_keyword": "!announce",
                "allowed_roles": [ 12345 ]
            }
        }

        self.mock_config = MockConfigurationService(mock_config_obj)

        self.mock_discord_service = Mock(DiscordService)

        self.announcement_service = AnnouncementService(self.mock_config, self.mock_discord_service)


class TestMakeAnnouncementUserHasRole(TestAnnouncementBase, TestCase):
    def setUp(self):
        TestAnnouncementBase.setUp(self)

    async def runTest(self):
        mock_role = create_mock_role(12345, "MyRole")
        mock_message = create_mock_message("!announce create operations This is an operation announcement", "the chan", [ mock_role ])
        await self.announcement_service.bot_command_callback(mock_message)

        self.mock_discord_service.send_channel_message.assert_called_with("This is an operation announcement", "operations")

class TestMakeAnnouncementUserDoesNotHaveRole(TestAnnouncementBase, TestCase):
    def setUp(self):
        TestAnnouncementBase.setUp(self)

    async def runTest(self):
        mock_message = create_mock_message("!announce create operations This is an operation announcement", "the chan")
        await self.announcement_service.bot_command_callback(mock_message)

        self.mock_discord_service.send_channel_message.assert_not_called()

class TestEditAnouncement(TestAnnouncementBase, TestCase):
    def setUp(self):
        TestAnnouncementBase.setUp(self)

        self.mock_message_to_edit = create_mock_message("the message", "the chan")
        
        self.mock_discord_service.get_matching_message = MagicMock(return_value=Future())
        self.mock_discord_service.get_matching_message.return_value.set_result(self.mock_message_to_edit)

    async def runTest(self):
        mock_role = create_mock_role(12345, "MyRole")
        mock_message = create_mock_message("!announce edit operations 12345 fixed announcement", "the chan", [ mock_role ])
        await self.announcement_service.bot_command_callback(mock_message)

        self.mock_discord_service.get_matching_message.assert_called_with("operations", 12345)
        self.mock_message_to_edit.edit.assert_called_with(content="fixed announcement")

class TestEditAnouncementWithoutRoles(TestAnnouncementBase, TestCase):
    def setUp(self):
        TestAnnouncementBase.setUp(self)

        self.mock_message_to_edit = create_mock_message("the message", "the chan")

    async def runTest(self):
        mock_message = create_mock_message("!announce edit operations 12345 fixed announcement", "the chan", [])
        await self.announcement_service.bot_command_callback(mock_message)

        self.mock_discord_service.get_matching_message.assert_not_called()
        self.mock_message_to_edit.edit.assert_not_called()

class TestSetReactionsOnAnnouncementWithRolesNoReactions(TestAnnouncementBase, TestCase):
    def setUp(self):
        TestAnnouncementBase.setUp(self)

        self.mock_role = create_mock_role(12345, "MyRole")

        self.mock_message_to_edit = create_mock_message("the message", "the chan", reactions=[])
        
        add_reaction_mock = MagicMock(return_value=Future())
        add_reaction_mock.return_value.set_result(None)
        type(self.mock_message_to_edit).add_reaction = add_reaction_mock

        self.mock_discord_service.get_matching_message = MagicMock(return_value=Future())
        self.mock_discord_service.get_matching_message.return_value.set_result(self.mock_message_to_edit)

    async def runTest(self):
        mock_command = create_mock_message("!announce seT-Reactions operations 987 👍 👎", "the chan", user_roles=[ self.mock_role ])

        await self.announcement_service.bot_command_callback(mock_command)

        self.mock_discord_service.get_matching_message.assert_called_with("operations", 987)
        
        self.mock_message_to_edit.add_reaction.assert_any_call("👍")
        self.mock_message_to_edit.add_reaction.assert_any_call("👎")