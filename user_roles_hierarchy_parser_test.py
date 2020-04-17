from unittest import TestCase
import json

from user_roles_hierarchy_parser import create_roles_dictionary

mock_config = json.loads("""
[
    {
        "role": "11111"
    },
    {
        "role": "22222",
        "sub_roles_access_channel": "33333",
        "sub_roles": [
            {
                "role": "44444"
            },
            {
                "role": "55555",
                "sub_roles_access_channel": "66666",
                "sub_roles": [
                    {
                        "role": "77777"
                    }
                ]
            }
        ]
    }
]
        """)

class TestGetSubRolesInTopLevelOfDictionary(TestCase):
    def setUp(self):
        self.default_channel = "21349280sdf23432"

    def test(self):
        channel_roles_dict = create_roles_dictionary(mock_config, self.default_channel)

        assert self.default_channel in channel_roles_dict
        default_channel_roles = channel_roles_dict[self.default_channel]

        assert len(default_channel_roles) == 2
        assert "11111" in default_channel_roles
        assert "22222" in default_channel_roles

        assert "33333" in channel_roles_dict
        three_sub_roles = channel_roles_dict["33333"]
        assert len(three_sub_roles) == 2
        assert "44444" in three_sub_roles
        assert "55555" in three_sub_roles

        assert "66666" in channel_roles_dict
        six_sub_roles = channel_roles_dict["66666"]
        assert len(six_sub_roles) == 1
        assert "77777" in six_sub_roles

class TestGettingRolesForUnsupportedChannelThrows(TestCase):
    def setUp(self):
        self.default_channel = "12345"

    def test(self):
        channel_roles_dict = create_roles_dictionary(mock_config, self.default_channel)

        self.assertRaises(KeyError, lambda: channel_roles_dict["sadfasfasdfsdfasd"])