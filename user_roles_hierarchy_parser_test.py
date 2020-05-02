from unittest import TestCase
import json

from user_roles_hierarchy_parser import create_roles_dictionary

mock_config = json.loads("""
[
    {
        "role": "1"
    },
    {
        "role": "2",
        "sub_roles_access_channel": "22222",
        "sub_roles": [
            {
                "role": "21"
            },
            {
                "role": "22",
                "sub_roles_access_channel": "33333",
                "sub_roles": [
                    {
                        "role": "221"
                    }
                ]
            },
            {
                "sub_roles_access_channel": "44444",
                "sub_roles": [
                    {
                        "role": "3"
                    }
                ]
            }
        ]
    },
    {
        "sub_roles_access_channel": "55555",
        "sub_roles": [
            {
                "role": "4"
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
        assert "1" in default_channel_roles
        assert "2" in default_channel_roles

        assert "22222" in channel_roles_dict
        two_sub_roles = channel_roles_dict["22222"]
        assert len(two_sub_roles) == 2
        assert "21" in two_sub_roles
        assert "22" in two_sub_roles

        assert "33333" in channel_roles_dict
        three_sub_roles = channel_roles_dict["33333"]
        assert len(three_sub_roles) == 1
        assert "221" in three_sub_roles

        assert "44444" in channel_roles_dict
        four_sub_roles = channel_roles_dict["44444"]
        assert len(four_sub_roles) == 1
        assert "3" in four_sub_roles

        assert "55555" in channel_roles_dict
        five_sub_roles = channel_roles_dict["55555"]
        assert len(five_sub_roles) == 1
        assert "4" in five_sub_roles

class TestGettingRolesForUnsupportedChannelThrows(TestCase):
    def setUp(self):
        self.default_channel = "12345"

    def test(self):
        channel_roles_dict = create_roles_dictionary(mock_config, self.default_channel)

        self.assertRaises(KeyError, lambda: channel_roles_dict["sadfasfasdfsdfasd"])