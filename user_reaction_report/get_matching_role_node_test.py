from asynctest import TestCase

from user_reaction_report.get_matching_role_node import get_matching_role_node

class TestBase:
    def setUp(self):
        self.structure = {
            "role_id": "1",
            "children": [
                {
                    "role_id": "2",
                    "children": [
                        {
                            "role_id": "3"
                        },
                        {
                            "role_id": "4"
                        }
                    ]
                },
                {
                    "role_id": "5"
                }
            ]
        }

class TestGetMatchingNode(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)

    def runTest(self):
        actual = get_matching_role_node("2", self.structure)
        
        assert actual["role_id"] == "2"
        assert len(actual["children"]) == 2
        assert actual["children"][0]["role_id"] == "3"
        assert actual["children"][1]["role_id"] == "4"

class TestGetMatchingRootNode(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)

    def runTest(self):
        actual = get_matching_role_node("1", self.structure)
        
        assert actual["role_id"] == "1"
        assert len(actual["children"]) == 2
        assert actual["children"][0]["role_id"] == "2"
        assert actual["children"][1]["role_id"] == "5"

class TestIsArrayBase:
    def setUp(self):
        self.structure = [
            {
                "role_id": "1"
            },
            {
                "role_id": "2",
                "children": [
                    {
                        "role_id": "3"
                    }
                ]
            }
        ]

class TestIsArrayBase1(TestIsArrayBase, TestCase):
    def setUp(self):
        TestIsArrayBase.setUp(self)
        
    def runTest(self):
        actual = get_matching_role_node("1", self.structure)

        assert actual["role_id"] == "1"

class TestIsArrayBase3(TestIsArrayBase, TestCase):
    def setUp(self):
        TestIsArrayBase.setUp(self)
        
    def runTest(self):
        actual = get_matching_role_node("3", self.structure)

        assert actual["role_id"] == "3"