from asynctest import TestCase

from user_reaction_report.message_splitter import split_message

class TestSplitSplitsByNewLine(TestCase):
    def setUp(self):
        self.split_token = "\n"
        self.message = "myMessage\nsplit"
        self.max_len = 12

    def runTest(self):
        actual = split_message(self.split_token, self.max_len, self.message)

        assert len(actual) == 2
        assert actual[0] == "myMessage"
        assert actual[1] == "split"

class TestNoSplitDueToLackOfNeed(TestCase):
    def setUp(self):
        self.split_token = "\n"
        self.message = "myMessage\nsplit"
        self.max_len = 200

    def runTest(self):
        actual = split_message(self.split_token, self.max_len, self.message)

        assert len(actual) == 1
        assert actual[0] == "myMessage\nsplit"