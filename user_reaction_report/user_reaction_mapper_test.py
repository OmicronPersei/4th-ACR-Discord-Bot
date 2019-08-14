from asynctest import TestCase, MagicMock, PropertyMock
from asyncio import Future

from user_reaction_report.user_reaction_mapper import map_message_to_user_reaction_dict

# reactions: dict of emoji: [(username, discriminator)]
def create_mock_message(emoji_dict):
    reactions = []
    for emoji,usernames in emoji_dict.items():
        mock_users = []
        for username in usernames:
            user_obj = MagicMock()
            type(user_obj).name = PropertyMock(return_value=username[0])
            type(user_obj).discriminator = PropertyMock(return_value=username[1])
            mock_users.append(user_obj)

        reaction = MagicMock()
        type(reaction).emoji = PropertyMock(return_value=emoji)
        reaction.users = MagicMock(return_value=Future())
        reaction.users.return_value.set_result(iter(mock_users))
        reactions.append(reaction)
    message = MagicMock()
    type(message).reactions = PropertyMock(return_value=reactions)
    return message
    

class TestUserReactionMapper(TestCase):
    def setUp(self):
        mock_reactions = dict()
        mock_reactions["👍"] = [("alpha", "1"), ("bravo", "2")]
        mock_reactions["👎"] = [("charlie", "3"), ("bravo", "2")]
        self.mock_message = create_mock_message(mock_reactions)

    async def runTest(self):
        actual = await map_message_to_user_reaction_dict(self.mock_message)
        # dict of username#discriminator: [emojis]
        assert "alpha#1" in actual
        assert len(actual["alpha#1"]) == 1
        assert "👍" in actual["alpha#1"]
        
        assert "bravo#2" in actual
        assert len(actual["bravo#2"]) == 2
        assert "👍" in actual["bravo#2"]
        assert "👎" in actual["bravo#2"]

        assert "charlie#3" in actual
        assert len(actual["charlie#3"]) == 1
        assert "👎" in actual["charlie#3"]
