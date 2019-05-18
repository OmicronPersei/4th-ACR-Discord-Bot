import unittest
from unittest.mock import MagicMock
from welcome_message import *
from discord import User

class Tests(unittest.TestCase):
    def test_sets_up_callback_for_discord_message(self):
        discord = MagicMock()
        join_callbacks = []
        discord.on_member_join_callbacks = join_callbacks
        
        WelcomeMessage(None, discord)

        assert len(join_callbacks) == 1
        assert callable(join_callbacks[0])

    def test_says_message_on_member_join_callback(self):
        discord = MagicMock()
        discord.on_member_join_callbacks = []
        discord.send_channel_message = MagicMock()
        config = {
            "message": "my message",
            "channel": "my channel"
        }
        user_joined = User(state=MagicMock(), data=MagicMock())
        WelcomeMessage(config, discord)

        callback = discord.on_member_join_callbacks[0]
        callback(user_joined)

        discord.send_channel_message.assert_called_once_with(message="my message", channel="my channel")




if __name__ == '__main__':
    unittest.main()
