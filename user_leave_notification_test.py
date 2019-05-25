import unittest
import asyncio
import asynctest
from unittest.mock import Mock, MagicMock, PropertyMock, call
import user_leave_notification
from test_utils import create_mock_user
from user_leave_notification import UserLeaveNotification
from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory

class TestUserLeaveNotificationAddsCallbackToDiscordOnMemberRemoveCallbacks(asynctest.TestCase):
    def setUp(self):
        self.config = {
            "message": "{left_user} has left",
            "channel": "user-left-channel"
        }
        self.discord = MagicMock()
        self.discord_mention_service = MagicMock()
        self.discord.on_member_remove_callbacks = []
        UserLeaveNotification(self.config, self.discord, self.discord_mention_service)

    def runTest(self):
        assert len(self.discord.on_member_remove_callbacks) == 1
        callback = self.discord.on_member_remove_callbacks[0]
        assert callable(callback)

class TestUserUserLeaveNotificationSendsMessageUponUserLeft(asynctest.TestCase):
    def setUp(self):
        self.config = {
            "message": "{left_user} has left",
            "channel": "user-left-channel"
        }
        self.discord = asynctest.Mock(DiscordService)
        self.discord.on_member_remove_callbacks = []
        self.mock_left_user = create_mock_user("lame_guy")

        self.discord_mention_service = MagicMock(DiscordMentionFactory)
        self.message_from_mention_factory = "generated message from factory"
        self.discord_mention_service.perform_replacement=MagicMock(return_value=self.message_from_mention_factory)

        UserLeaveNotification(self.config, self.discord, self.discord_mention_service)

    async def runTest(self):
        callback = self.discord.on_member_remove_callbacks[0]
        await callback(self.mock_left_user)

        self.discord_mention_service.perform_replacement.assert_called_with("{user:0} has left", [self.mock_left_user])
        self.discord.send_channel_message.assert_called_with(self.message_from_mention_factory, "user-left-channel")