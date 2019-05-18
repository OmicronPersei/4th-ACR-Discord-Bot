import unittest
from unittest.mock import MagicMock
from welcome_message import *

class Tests(unittest.TestCase):
    
    def test_sets_up_callback_for_discord_message(self):
        discord = MagicMock()
        join_callbacks = []
        discord.on_member_join_callbacks = join_callbacks
        
        welcome_message(None, discord)

        #discord.on_member_join_callbacks.assert_called()
        assert len(join_callbacks) == 1
        assert callable(join_callbacks[0])


if __name__ == '__main__':
    unittest.main()
