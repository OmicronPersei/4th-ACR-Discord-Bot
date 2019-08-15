from asynctest import MagicMock, TestCase, PropertyMock
from asyncio import Future

from user_reaction_report.user_reaction_report import UserReactionReport

from test_utils import MockConfigurationService
from user_reaction_report.test_utils import create_mock_message as create_mock_message_with_emojis, create_mock_role, create_mock_user, AsyncIterator

def create_mock_message(msg_content, channel_name):
    mock_message = MagicMock()
    type(mock_message).content = PropertyMock(return_value=msg_content)
    
    mock_channel = MagicMock()
    type(mock_channel).name = PropertyMock(return_value=channel_name)
    type(mock_message).channel = PropertyMock(return_value=mock_channel)

    return mock_message 


class TestUserReactionReport(TestCase):
    def setUp(self):
        self.mock_config = MockConfigurationService({
            "user_reaction_reporter": {
                "enabled": True,
                "command_keyword": "!expected-attendance",
                "restrict_to_channel": "the-attendance-chan",
                "emojis": [
                    { "emoji": "👍", "display_template": "**{user}** ({role})" },
                    { "emoji": "👎", "display_template": "~~{user}~~ ({role})" },
                    { "emoji": "", "display_template": "!!{user}!! ({role})" }
                ],
                "role_aliases": {
                    "123": "1"
                },
                "role_structure": {
                    "role_id": "1",
                    "children": [
                        {
                            "role_id": "2"
                        },
                        {
                            "role_id": "3"
                        }
                    ]
                }
            }
        })
        self.mock_discord_service = MagicMock()
        emoji_dict_responses = dict()
        emoji_dict_responses["👍"] = [
            create_mock_user(display_name_val="Alpha", id=111),
            create_mock_user(display_name_val="Bravo", id=222)
        ]
        emoji_dict_responses["👎"] = [
            create_mock_user(display_name_val="Charlie", id=333)
        ]
        msg_with_reactions = create_mock_message_with_emojis(emoji_dict_responses)

        self.mock_discord_service.get_matching_message = MagicMock(return_value=Future())
        self.mock_discord_service.get_matching_message.return_value.set_result(msg_with_reactions)

        self.mock_discord_service.get_matching_role = MagicMock(return_value=create_mock_role(123, "mock-role"))

        role1 = create_mock_role(1, "High")
        role2 = create_mock_role(2, "Low")
        role3 = create_mock_role(3, "Very Low")

        mock_members = [
            create_mock_user(display_name_val="Alpha", id=111, roles=[role1]),
            create_mock_user(display_name_val="Bravo", id=222, roles=[role2]),
            create_mock_user(display_name_val="Charlie", id=333, roles=[role2]),
            create_mock_user(display_name_val="Delta", id=444, roles=[role3]),
        ]
        def member_generator():
            for m in mock_members:
                yield m    

        type(self.mock_discord_service).get_all_members = PropertyMock(return_value=member_generator)

        self.mock_discord_service.get_all_roles = MagicMock(return_value=[
            role1, role2, role3
        ])
        
        self.mock_discord_service.send_channel_message = MagicMock(return_value=Future())
        self.mock_discord_service.send_channel_message.return_value.set_result(None)

        self.mock_discord_service.create_listener_for_bot_command = MagicMock()

        self.user_reaction_report = UserReactionReport(self.mock_discord_service, self.mock_config)



    async def runTest(self):
        cmd = "!expected-attendance operations 112358 1st platoon"
        mock_cmd = create_mock_message(cmd, "the-attendance-chan")

        expected = (
            "**Alpha** (High)\n"
            "     **Bravo** (Low)\n"
            "     ~~Charlie~~ (Low)\n"
            "     !!Delta!! (Very Low)"
        )

        await self.user_reaction_report.bot_command_callback(mock_cmd)

        self.mock_discord_service.get_matching_message.assert_called_with("operations", 112358)
        self.mock_discord_service.get_matching_role.assert_called_with("1st platoon")
        self.mock_discord_service.get_all_roles.assert_called()
        self.mock_discord_service.send_channel_message.assert_called_with(expected, "the-attendance-chan")
        # assert self.send_channel_message_Future.done()