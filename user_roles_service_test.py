from asyncio import Future
import json
from asynctest import MagicMock, TestCase, PropertyMock
from user_roles_service import UserRolesService


from test_utils import MockConfigurationService, create_mock_message

def create_mock_role(role_props):
    role = MagicMock()
    type(role).name = role_props["name"]
    type(role).id = role_props["id"]
    return role

class BaseTestSetup:
    def setUp(self):
        self.mock_discord_service = MagicMock()
        self.mock_discord_service.create_listener_for_bot_command.side_effect = self.create_callback_side_effect

        self.politics_role = create_mock_role({ "name": "politics", "id": 1111 })
        self.funstuff_role = create_mock_role({ "name": "Fun-stuff", "id": 2222 })
        self.starcraft_role = create_mock_role({ "name": "Starcraft", "id": 3333 })
        self.all_mock_roles = [
            self.politics_role,
            self.funstuff_role,
            self.starcraft_role
        ]

        self.mock_discord_service.get_all_roles = MagicMock(return_value=self.all_mock_roles)

        self.mock_discord_service.send_channel_message = MagicMock(return_value=Future())
        self.mock_discord_service.send_channel_message.return_value.set_result(None)

        self.mock_config = json.loads('''
                {
                    "user_role_self_service": {
                        "command_keyword": "!roles",
                        "main_request_channel": "9999",
                        "available_roles": [
                            {
                                "role": "1111",
                                "sub_roles_accessable_channel": "0239043989",
                                "sub_roles": [
                                    {
                                        "role": "3333"
                                    }
                                ]
                            },
                            {
                                "role": "2222"
                            }
                        ]
                    }
                }
            ''')

        self.mock_config_service = MockConfigurationService(self.mock_config)

        self.mock_roles_availabe_provider = MagicMock()

        self.user_roles_service = UserRolesService(self.mock_config_service, self.mock_discord_service, self.mock_roles_availabe_provider)

    def create_callback_side_effect(self, *args, **kwargs):
        self.callback = args[1]

    def get_mock_role(self, name):
        return [x for x in self.all_mock_roles if x.name.lower() == name.lower()][0]


class TestReturnsAvailableRolesWhenCalledWithAvailableRoles(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_roles_availabe_provider.get_roles_for_message = MagicMock(return_value=[self.politics_role, self.funstuff_role])
        self.mock_message = create_mock_message("!roles", channel_id=9999)

    async def runTest(self):
        await self.callback(self.mock_message)

        expected_message = "Roles available:\n`politics`\n`Fun-stuff`"
        expected_channel_id = 9999
        self.mock_discord_service.send_channel_message.assert_called_with(expected_message, channel_id=expected_channel_id)

class TestReturnsAvailableRolesWhenCalledWithNoAvailableRoles(BaseTestSetup, TestCase):
    def setUp(self):
        BaseTestSetup.setUp(self)
        self.mock_roles_availabe_provider.get_roles_for_message = MagicMock(return_value=[])
        self.mock_message = create_mock_message("!roles", channel_id=9999)

    async def runTest(self):
        await self.callback(self.mock_message)

        self.mock_discord_service.send_channel_message.assert_not_called()

