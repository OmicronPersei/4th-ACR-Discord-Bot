# from asynctest import MagicMock, TestCase
# from asyncio import Future

# from user_reaction_report.user_reaction_report import UserReactionReport

# from test_utils import MockConfigurationService

# class TestUserReactionReport(TestCase):
#     def setUp(self):
#         self.mock_config = MockConfigurationService({
#             "user_reaction_reporter": {
#                 "enabled": True,
#                 "command_keyword": "!expected-attendance",
#                 "restrict-to-channel": "expected-attendance",
#                 "emojis": [
#                     { "emoji": "👍", "display_template": "**{user} ({name})**" },
#                     { "emoji": "👎", "display_template": "~~{user} ({name})~~" },
#                 ]
#             }
#         })
#         self.mock_discord_service = MagicMock()
