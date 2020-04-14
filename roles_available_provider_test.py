from unittest import TestCase, main
from unittest.mock import MagicMock, call
import json

from test_utils import create_mock_user, create_mock_role, create_mock_message

from roles_available_provider import RolesAvailableProvider

mock_config = json.loads('''
{
    "available_roles": [
        {
            "role": "45645646545465",
            "sub_roles_accessable_channel": "234324324234",
            "sub_roles": [
                {
                    "role": "2342323423"
                }
            ]
        }
    ],
    "command_keyword": "!roles",
    "enabled": true,
    "main_request_channel": "98749874954984"
}
''')

class TestGetsRoles(TestCase):
    def setUp(self):
        self.mock_chan_id = 381231232
        mock_role_dict = dict()
        mock_role_dict[str(self.mock_chan_id)] = [ "11111", "22222" ]
        self.mock_user_roles_hierarchy_parser = MagicMock(return_value=mock_role_dict)

        self.mock_config_service = MagicMock()
        self.mock_config_service.get = MagicMock(return_value=mock_config)

        self.sent_msg = create_mock_message("!roles", None, channel_id=self.mock_chan_id)

        self.mock_discord_service = MagicMock()
        self.mock_discord_service.get_role_by_id.side_effect = self.get_role_by_id_sideeffect

        self.roles_available_provider = RolesAvailableProvider(self.mock_user_roles_hierarchy_parser, self.mock_discord_service, self.mock_config_service)

    def get_role_by_id_sideeffect(self, *args, **kwargs):
        if args[0] == 11111:
            return create_mock_role(11111, "MyRole1")
        elif args[0] == 22222:
            return create_mock_role(22222, "MyRole2")

        

    def test(self):
        actual = self.roles_available_provider.get_roles_for_message(self.sent_msg)

        self.mock_config_service.get.assert_called_with("user_role_self_service")
        self.mock_user_roles_hierarchy_parser.assert_called_with(mock_config["available_roles"], mock_config["main_request_channel"])
        expected_calls = [ call(11111), call(22222) ]
        self.mock_discord_service.get_role_by_id.assert_has_calls(calls=expected_calls, any_order=True)
        
        assert len(actual) == 2
        assert len([x for x in actual if x.id == 11111 and x.name == "MyRole1"]) == 1
        assert len([x for x in actual if x.id == 22222 and x.name == "MyRole2"]) == 1

class TestGetsRolesFails(TestCase):
    def setUp(self):
        self.mock_chan_id = 381231232
        
        self.mock_user_roles_hierarchy_parser = MagicMock()
        self.mock_user_roles_hierarchy_parser.side_effect = KeyError()

        self.mock_config_service = MagicMock()
        self.mock_config_service.get = MagicMock(return_value=mock_config)

        self.sent_msg = create_mock_message("!roles", None, channel_id=self.mock_chan_id)

        self.mock_discord_service = MagicMock()

        self.roles_available_provider = RolesAvailableProvider(self.mock_user_roles_hierarchy_parser, self.mock_discord_service, self.mock_config_service)

    def test(self):
        actual = self.roles_available_provider.get_roles_for_message(self.sent_msg)

        self.mock_config_service.get.assert_called_with("user_role_self_service")
        self.mock_user_roles_hierarchy_parser.assert_called_with(mock_config["available_roles"], mock_config["main_request_channel"])
        
        self.mock_discord_service.get_role_by_id.assert_not_called()
        
        assert len(actual) == 0