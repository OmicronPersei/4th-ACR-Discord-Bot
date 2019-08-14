from asynctest import TestCase

from user_reaction_report.serialize_reaction_tree import serialize_reaction_tree

from user_reaction_report.test_utils import create_mock_role, create_mock_user

class TestSerializeReactionTree(TestCase):
    def setUp(self):
        self.mock_roles = [
            create_mock_role(1, "Higher Up"),
            create_mock_role(2, "Lower"),
            create_mock_role(3, "Very Low")
        ]
        self.mock_reaction_tree = {
            "role_id": "1",
            "reactions": [
                {
                    "user": create_mock_user(id=1111, display_name_val="Alpha"),
                    "emoji": "👍"
                }
            ],
            "children": [
                {
                    "role_id": "2",
                    "reactions": [
                        {
                            "user": create_mock_user(id=2222, display_name_val="Bravo"),
                            "emoji": "👍"
                        },
                        {
                            "user": create_mock_user(id=3333, display_name_val="Charlie"),
                            "emoji": "👎"
                        }
                    ],
                    "children": [
                        {
                            "role_id": "3",
                            "reactions": [
                                {
                                    "user": create_mock_user(id=4444, display_name_val="Delta"),
                                    "emoji": "👍"
                                },
                                {
                                    "user": create_mock_user(id=5555, display_name_val="Foxtrot"),
                                    "emoji": ""
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        self.mock_emoji_templates = [
            { "emoji": "👍", "display_template": "**{user}** ({role})"},
            { "emoji": "👎", "display_template": "~~{user}~~ ({role})"},
            { "emoji": "", "display_template": "!!{user}!! ({role})"}
        ]
    
    def runTest(self):
        actual = serialize_reaction_tree(self.mock_reaction_tree, self.mock_emoji_templates, self.mock_roles)
        expected = (
            "**Alpha** (Higher Up)\n"
            "     **Bravo** (Lower)\n"
            "     ~~Charlie~~ (Lower)\n"
            "          **Delta** (Very Low)\n"
            "          !!Foxtrot!! (Very Low)")
        assert actual == expected

