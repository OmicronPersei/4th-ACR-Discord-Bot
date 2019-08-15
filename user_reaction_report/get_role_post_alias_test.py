from asynctest import TestCase, MagicMock

from user_reaction_report.get_role_post_alias import get_role_post_alias

class TestBase:
    def setUp(self):
        self.mock_config = {
            "role_aliases": {
                "123": "456"
            }
        }


class TestRoleReplacedWithAlias(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)
        
    def runTest(self):
        expected = "456"
        actual = get_role_post_alias("123", self.mock_config)
        
        assert actual == expected


class TestRoleNotReplacedWithAlias(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)
        
    def runTest(self):
        expected = "789"
        actual = get_role_post_alias("789", self.mock_config)
        
        assert actual == expected
        