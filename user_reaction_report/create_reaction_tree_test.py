from asynctest import TestCase, main

from user_reaction_report.create_reaction_tree import create_reaction_tree

from user_reaction_report.test_utils import create_mock_user, create_mock_role

class TestCreateReactionTree(TestCase):
    def setUp(self):
        self.structure = {
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
        self.mock_reactions = {
            "1111": { "user": create_mock_user(id=1111), "emojis": [ "👍" ] },
            "2222": { "user": create_mock_user(id=2222), "emojis": [ "👎" ] },
            "3333": { "user": create_mock_user(id=3333), "emojis": [ "🤷" ] },
            "4444": { "user": create_mock_user(id=4444), "emojis": [ "👎", "🤷" ] }
        }
        role1 = create_mock_role(1, "MyRole1")
        role2 = create_mock_role(2, "MyRole2")
        role3 = create_mock_role(3, "MyRole3")
        role4 = create_mock_role(4, "MyRole4")

        self.mock_all_users = [
            create_mock_user(id=1111, roles=[role1]),
            create_mock_user(id=2222, roles=[role2]),
            create_mock_user(id=3333, roles=[role2]),
            create_mock_user(id=4444, roles=[role3]),
            create_mock_user(id=5555, roles=[role3]),
            create_mock_user(id=6666, roles=[role4])
        ]

    def runTest(self):
        # expected shape
        # {
        #    "role_id": "1",
        #    "reactions": [
        #       { "user": obj, "emoji": "👍" }    
        # ]
        # }
        actual = create_reaction_tree(self.structure, self.mock_all_users, self.mock_reactions)

        role1_node = actual
        assert role1_node["role_id"] == "1"
        assert len(role1_node["reactions"]) == 1
        assert role1_node["reactions"][0]["user"].id == 1111
        assert role1_node["reactions"][0]["emoji"] == "👍"

        assert len(actual["children"]) == 2

        role2_node = actual["children"][0]
        assert role2_node["role_id"] == "2"
        assert len(role2_node["reactions"]) == 2
        assert role2_node["reactions"][0]["user"].id == 2222
        assert role2_node["reactions"][0]["emoji"] == "👎"
        assert role2_node["reactions"][1]["user"].id == 3333
        assert role2_node["reactions"][1]["emoji"] == "🤷"

        role3_node = actual["children"][1]
        assert role3_node["role_id"] == "3"
        assert len(role3_node["reactions"]) == 0


main()