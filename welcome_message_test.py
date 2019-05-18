import unittest
import asyncio
import asynctest
from unittest.mock import Mock, MagicMock, PropertyMock, call
from welcome_message import WelcomeMessage
from discord_service import DiscordService

def create_mock_user(mention_val):
    mock_user = MagicMock()
    type(mock_user).mention = PropertyMock(return_value=mention_val)
    return mock_user

class TestConstructionSubscribesToOnMemberJoinCallback(asynctest.TestCase):
    def setUp(self):
        self.discord = MagicMock()
        self.join_callbacks = []
        self.discord.on_member_join_callbacks = self.join_callbacks

    def test(self):
        WelcomeMessage(None, self.discord)

        assert len(self.join_callbacks) == 1
        assert callable(self.join_callbacks[0])

class TestSendsChannelMessageUponOnMemberJoinCallback(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())
        self.discord.on_member_join_callbacks = []
        self.config = {
            "message": "my message",
            "channel": "my channel"
        }
        self.user_joined = create_mock_user("val")
        WelcomeMessage(self.config, self.discord)

    async def test(self):
        callback = self.discord.on_member_join_callbacks[0]
        await callback(self.user_joined)

        self.discord.send_channel_message.assert_called_once_with("my message", "my channel")

class TestSendsChannelMessageUponOnMemberJoinCallbackWithUsernameReplacedWithMentions(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())
        self.discord.on_member_join_callbacks = []
        self.discord.send_channel_message = MagicMock()
        self.discord.send_channel_message.return_value = asyncio.Future()
        self.discord.send_channel_message.return_value.set_result(None)

        self.mock_user_exe_mention="<exe_str>"
        self.mock_user_Exe = create_mock_user(self.mock_user_exe_mention)
        self.mock_user_dabele_mention="<abele_str>"
        self.mock_user_DAbele = create_mock_user(self.mock_user_dabele_mention)

        self.mock_joining_user = create_mock_user("val")
        
        self.discord.get_matching_Member = MagicMock()
        self.discord.get_matching_Member.side_effect = self.get_matching_member_side_effect
        
        config = {
            "message": "{member:Exe#1234} welcomes you!  Unit of {member:D. Abele#789}",
            "channel": "my channel"
        }
        WelcomeMessage(config, self.discord)

    def get_matching_member_side_effect(self, *args, **kwargs):
        if args[0] == "Exe" and args[1] == "1234":
            return self.mock_user_Exe
        elif args[0] == "D. Abele" and args[1] == "789":
            return self.mock_user_DAbele

    async def test(self):
        callback = self.discord.on_member_join_callbacks[0]
        await callback(self.mock_joining_user)

        mock = self.discord.get_matching_Member
        expected_calls = [call("Exe", "1234"), call("D. Abele", "789")]
        mock.assert_has_calls(expected_calls, any_order=True)

        expected_message = "{} welcomes you!  Unit of {}".format(self.mock_user_exe_mention, self.mock_user_dabele_mention)
        expected_channel = "my channel"
        self.discord.send_channel_message.assert_called_once_with(expected_message, expected_channel)

class TestSendsChannelMessageUponJoinCallbackAndResolvesJoiningUser(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())
        self.discord.on_member_join_callbacks = []
        self.discord.send_channel_message = MagicMock()
        self.discord.send_channel_message.return_value = asyncio.Future()
        self.discord.send_channel_message.return_value.set_result(None)

        self.mock_joining_user_mention_val = "<val!>"
        self.mock_joining_user = create_mock_user(self.mock_joining_user_mention_val)
        
        config = {
            "message": "Welcome, {joined_user}!",
            "channel": "my channel"
        }
        WelcomeMessage(config, self.discord)

    async def test(self):
        callback = self.discord.on_member_join_callbacks[0]
        await callback(self.mock_joining_user)

        self.discord.get_matching_Member.assert_not_called()

        expected_message = "Welcome, {}!".format(self.mock_joining_user_mention_val)
        expected_channel = "my channel"
        self.discord.send_channel_message.assert_called_once_with(expected_message, expected_channel)

class TestWelcomeMessageResolvesRoleMention(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())
        self.discord.on_member_join_callbacks = []
        self.discord.send_channel_message = MagicMock()
        self.discord.send_channel_message.return_value = asyncio.Future()
        self.discord.send_channel_message.return_value.set_result(None)

        self.mock_joining_user = create_mock_user("<val>")

        matching_role = MagicMock()
        type(matching_role).mention = PropertyMock(return_value="<rolestr>")
        self.discord.get_matching_role = MagicMock(return_value=matching_role)
        
        config = {
            "message": "Please message a {role:Recruiter}!",
            "channel": "my channel"
        }
        WelcomeMessage(config, self.discord)

    async def test(self):
        callback = self.discord.on_member_join_callbacks[0]
        await callback(self.mock_joining_user)

        expected_message = "Please message a <rolestr>!"
        expected_channel = "my channel"
        self.discord.get_matching_role.assert_called_once_with("Recruiter")
        self.discord.send_channel_message.assert_called_once_with(expected_message, expected_channel)


if __name__ == '__main__':
    unittest.main()
