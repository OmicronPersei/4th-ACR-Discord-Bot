from unittest import TestCase
from unittest.mock import MagicMock, call
import json

from test_utils import create_mock_user, create_mock_role, create_mock_message

from roles_available_provider import RolesAvailableProvider

mock_config = json.loads('''
{
    "channels_available_roles": {
        "11111": [
            "1",
            "2"
        ]
    },
    "command_keyword": "!roles"
}
''')

class TestGetsRoles(TestCase):
    def setUp(self):
        self.mock_chan_id = 11111

        self.mock_config_service = MagicMock()
        self.mock_config_service.get = MagicMock(return_value=mock_config)

        self.sent_msg = create_mock_message("!roles", None, channel_id=self.mock_chan_id)

        self.mock_discord_service = MagicMock()
        self.mock_discord_service.get_role_by_id.side_effect = self.get_role_by_id_sideeffect

        self.roles_available_provider = RolesAvailableProvider(self.mock_discord_service, self.mock_config_service)

    def get_role_by_id_sideeffect(self, *args, **kwargs):
        if args[0] == 1:
            return create_mock_role(1, "MyRole1")
        elif args[0] == 2:
            return create_mock_role(2, "MyRole2")

    def test(self):
        actual = self.roles_available_provider.get_roles_for_message(self.sent_msg)

        self.mock_config_service.get.assert_called_with("user_role_self_service")
        expected_calls = [ call(1), call(2) ]
        self.mock_discord_service.get_role_by_id.assert_has_calls(calls=expected_calls, any_order=True)
        
        assert len(actual) == 2
        assert len([x for x in actual if x.id == 1 and x.name == "MyRole1"]) == 1
        assert len([x for x in actual if x.id == 2 and x.name == "MyRole2"]) == 1

class TestGetsRolesFails(TestCase):
    def setUp(self):
        self.mock_chan_id = 381231232

        self.mock_config_service = MagicMock()
        self.mock_config_service.get = MagicMock(return_value=mock_config)

        self.sent_msg = create_mock_message("!roles", None, channel_id=self.mock_chan_id)

        self.mock_discord_service = MagicMock()

        self.roles_available_provider = RolesAvailableProvider(self.mock_discord_service, self.mock_config_service)

    def test(self):
        actual = self.roles_available_provider.get_roles_for_message(self.sent_msg)

        self.mock_config_service.get.assert_called_with("user_role_self_service")
        
        self.mock_discord_service.get_role_by_id.assert_not_called()
        
        assert len(actual) == 0