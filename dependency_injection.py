from dependency_injector import providers

from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory
from user_leave_notification import UserLeaveNotification
from welcome_message import WelcomeMessage
from sql_wrapper import SQLWrapper
from forum_thread_data_storage import ForumThreadDataStorage

class Dependencies:
    def __init__(self, config):
        super().__init__()
        self.config = providers.Configuration("config")
        self.config.override(config)

        self.discord_service = providers.Singleton(DiscordService)
        self.discord_mention_factory = providers.Singleton(DiscordMentionFactory, self.discord_service)
        self.welcome_message = providers.Singleton(WelcomeMessage, self.config.welcome_message, self.discord_service, self.discord_mention_factory)
        self.user_leave_notification = providers.Singleton(UserLeaveNotification, self.config.user_leave_notification, self.discord_service, self.discord_mention_factory)
        self.sql_wrapper = providers.Singleton(SQLWrapper, self.config)
        # self.forum_thread_data_storage = providers.Singleton(ForumThreadDataStorage, self.config.xen_foro_integration)

