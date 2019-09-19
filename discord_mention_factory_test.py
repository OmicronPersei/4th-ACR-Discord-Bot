import unittest
import asyncio
import asynctest
from unittest.mock import Mock, MagicMock, PropertyMock, call
from discord_mention_factory import DiscordMentionFactory
from discord_service import DiscordService
from test_utils import create_mock_user

class TestReplacesUserAndDiscriminatorWithCorrespondingDiscordMemberMention(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())
        self.discord_mention_factory = DiscordMentionFactory(self.discord)

        self.mock_user_one_mention="<one_str>"
        self.mock_user_one = create_mock_user(self.mock_user_one_mention)
        self.mock_user_two_mention="<two_str>"
        self.mock_user_two = create_mock_user(self.mock_user_two_mention)
        
        self.discord.get_matching_Member = MagicMock()
        self.discord.get_matching_Member.side_effect = self.get_matching_member_side_effect
        
        self.message_template = "{member:One#1234} welcomes you!  Unit of {member:Two#789}"

    def get_matching_member_side_effect(self, *args, **kwargs):
        if args[0] == "One" and args[1] == "1234":
            return self.mock_user_one
        elif args[0] == "Two" and args[1] == "789":
            return self.mock_user_two

    async def test(self):
        actual_message = self.discord_mention_factory.perform_replacement(self.message_template)
        expected_message = "{} welcomes you!  Unit of {}".format(self.mock_user_one_mention, self.mock_user_two_mention)
        
        mock = self.discord.get_matching_Member
        expected_calls = [call("One", "1234"), call("Two", "789")]
        mock.assert_has_calls(expected_calls, any_order=True)

        
        assert actual_message == expected_message

class TestReplacesListOfUsersWithCorrespondingDiscordMentions(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())

        self.discord_mention_factory=DiscordMentionFactory(self.discord)

        self.mock_joining_user0_mention_val = "<val!>"
        self.mock_joining_user0 = create_mock_user(self.mock_joining_user0_mention_val)

        self.mock_joining_user1_mention_val = "dfasdf"
        self.mock_joining_user1 = create_mock_user(self.mock_joining_user1_mention_val)

        self.mock_joining_user2_mention_val = "sdfs"
        self.mock_joining_user2_display_name = "display_name_here"
        self.mock_joining_user2 = create_mock_user(self.mock_joining_user2_mention_val, self.mock_joining_user2_display_name)
        
        self.message_template = "yo {user:0} and {user:1} and {user:display_name:2}"

    async def test(self):
        actual_message = self.discord_mention_factory.perform_replacement(self.message_template, [self.mock_joining_user0, self.mock_joining_user1, self.mock_joining_user2])
        expected_message = "yo {} and {} and {}".format(self.mock_joining_user0_mention_val, self.mock_joining_user1_mention_val, self.mock_joining_user2_display_name)

        assert actual_message == expected_message

class TestReplacesRolesWithCorrespondingDiscordMentions(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())

        self.discord_mention_factory = DiscordMentionFactory(self.discord)

        self.mock_joining_user = create_mock_user("<val>")

        matching_role = MagicMock()
        type(matching_role).mention = PropertyMock(return_value="<rolestr>")
        self.discord.get_matching_role = MagicMock(return_value=matching_role)
        
        self.message_template = "Please message a {role:Recruiter}!"

    async def test(self):
        actual_message = self.discord_mention_factory.perform_replacement(self.message_template)
        expected_message = "Please message a <rolestr>!"

        self.discord.get_matching_role.assert_called_once_with("Recruiter")
        
        assert actual_message == expected_message

class TestReplacesChannelMention(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())

        self.discord_mention_factory = DiscordMentionFactory(self.discord)

        matching_channel = MagicMock()
        type(matching_channel).mention = PropertyMock(return_value="<channelVal>")
        self.discord.get_matching_channel = MagicMock(return_value=matching_channel)

        self.message_template = "Please see us in {channel:the-channel}"

    def test(self):
        actual_message = self.discord_mention_factory.perform_replacement(self.message_template)
        expected_message = "Please see us in <channelVal>"

        self.discord.get_matching_channel.assert_called_once_with("the-channel")

        assert actual_message == expected_message