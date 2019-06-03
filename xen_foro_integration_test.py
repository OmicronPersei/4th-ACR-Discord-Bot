from asynctest import MagicMock, TestCase

from sql_wrapper import SQLWrapper
from xen_foro_forum_thread_url_factory import XenForoForumThreadURLFactory
from xen_foro_new_message_dispatcher import XenForoNewMessageDispatcher
from xen_foro_new_thread_detector import XenForoNewThreadDetector
from xen_foro_request_factory import XenForoRequestFactory
from xen_foro_thread_getter import XenForoThreadGetter
from forum_thread_data_storage import ForumThreadDataStorage
from discord_mention_factory import DiscordMentionFactory

mock_config = {
    "welcome_message": {
        "message": "the message",
        "channel": "welcome message channel",
        "enabled": True
    },
    "user_leave_notification": {
        "message": "the message",
        "channel": "user leave channel",
        "enabled": True
    },
    "db_filename": ":memory:",
    "xen_foro_integration": {
        "forum_name": "my_unique_prefix",
        "base_url": "https://myforum.xyz/",
        "update_period": "60",
        "forums": [
            {
                "forum_id": "234",
                "target_discord_channel": "forum posts",
                "message_template": "A new forum post has appeared! {thread_url}",
                "discord_message_emojis": []
            }
        ]
    }
}

mock_secrets = {
    "xen_foro_integration_api_token": "imsecret"
}

class MockSQLWrapper(SQLWrapper):
    def __init__(self, config, mock_sql):
        super().__init__(config)
        self.mock_sql = mock_sql

    def _get_db_connection(self, db_filename):
        return self.mock_sql

class XenForoIntegrationTest(TestCase):
    def setUp(self):
        self.mock_sql = MagicMock()
        self.mock_sql_wrapper = MockSQLWrapper(mock_config, self.mock_sql)

        self.forum_url_factory = XenForoForumThreadURLFactory()

        self.request_factory = XenForoRequestFactory()

        self.thread_getter = XenForoThreadGetter(self.request_factory)

        self.forum_data_storage = ForumThreadDataStorage(self.mock_sql_wrapper)

        xen_forum_config = mock_config["xen_foro_integration"]
        xen_forum_api_token = mock_secrets["xen_foro_integration_api_token"]
        self.new_thread_detector = XenForoNewThreadDetector(self.thread_getter, self.thread_data_storage, xen_forum_config, xen_forum_api_token)

        self.discord_service = MagicMock()
        self.discord_service.send_channel_message = MagicMock()

        self.discord_mention_factory = DiscordMentionFactory(self.discord_service)

        self.new_thread_dispatcher = XenForoNewMessageDispatcher(self.new_thread_detector, self.discord_service, self.discord_mention_factory, self.forum_data_storage, self.forum_thread_url_factory, xen_forum_config)


