import unittest
import asyncio
import asynctest
from unittest.mock import Mock, MagicMock, PropertyMock, call
from welcome_message import WelcomeMessage
from discord_service import DiscordService
from test_utils import create_mock_user
from discord_mention_factory import DiscordMentionFactory

class TestConstructionSubscribesToOnMemberJoinCallback(asynctest.TestCase):
    def setUp(self):
        self.discord = MagicMock()
        self.join_callbacks = []
        self.discord.on_member_join_callbacks = self.join_callbacks
        self.discord_mention_service = asynctest.Mock(DiscordMentionFactory(None))

    def test(self):
        WelcomeMessage(None, self.discord, self.discord_mention_service)

        assert len(self.join_callbacks) == 1
        assert callable(self.join_callbacks[0])

class TestSendsChannelMessageUponOnMemberJoinCallback(asynctest.TestCase):
    def setUp(self):
        self.discord = asynctest.Mock(DiscordService())
        self.discord.on_member_join_callbacks = []
        self.config = {
            "message": "my message {joined_user}",
            "channel": "my channel"
        }
        self.mock_user_joined = create_mock_user("val")
        self.returned_message = "dsfasf"
        self.discord_mention_service = asynctest.Mock(DiscordMentionFactory(None))
        self.discord_mention_service.perform_replacement=MagicMock(return_value=self.returned_message)
        WelcomeMessage(self.config, self.discord, self.discord_mention_service)

    async def test(self):
        callback = self.discord.on_member_join_callbacks[0]
        await callback(self.mock_user_joined)

        self.discord_mention_service.perform_replacement.assert_called_with("my message {user:0}", [self.mock_user_joined])
        self.discord.send_channel_message.assert_called_once_with(self.returned_message, "my channel")

