from dependency_injector import providers

from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory
from user_leave_notification import UserLeaveNotification
from welcome_message import WelcomeMessage
from sql_wrapper import SQLWrapper
from forum_thread_data_storage import ForumThreadDataStorage
from xen_foro_request_factory import XenForoRequestFactory
from xen_foro_thread_getter import XenForoThreadGetter
from xen_foro_new_thread_detector import XenForoNewThreadDetector
from xen_foro_new_message_dispatcher import XenForoNewMessageDispatcher

class Dependencies:
    def __init__(self, config, secrets):
        super().__init__()
        self.config = providers.Configuration("config")
        self.config.override(config)

        self.secrets = providers.Configuration("config")
        self.secrets.override(secrets)

        self.discord_service = providers.Singleton(DiscordService)
        self.discord_mention_factory = providers.Singleton(DiscordMentionFactory, self.discord_service)
        self.welcome_message = providers.Singleton(WelcomeMessage, self.config.welcome_message, self.discord_service, self.discord_mention_factory)
        self.user_leave_notification = providers.Singleton(UserLeaveNotification, self.config.user_leave_notification, self.discord_service, self.discord_mention_factory)
        self.sql_wrapper = providers.Singleton(SQLWrapper, self.config)
        self.forum_thread_data_storage = providers.Singleton(ForumThreadDataStorage, self.sql_wrapper)
        self.xen_foro_request_factory = providers.Singleton(XenForoRequestFactory)
        self.xen_foro_thread_getter = providers.Singleton(XenForoThreadGetter, self.xen_foro_request_factory)
        self.xen_foro_new_thread_detector = providers.Singleton(XenForoNewThreadDetector, self.xen_foro_thread_getter, self.forum_thread_data_storage, self.config.xen_foro_integration, self.secrets.xen_foro_integration_api_token)
        #def __init__(self, xen_foro_new_thread_detector, discord_service, discord_mention_factory, forum_thread_data_storage, clock_signal, forum_thread_url_factory, config)
        # self.xen_foro_new_message_dispatcher = providers.Singleton(XenForoNewMessageDispatcher, self.xen_foro_new_thread_detector, self.discord_service, self.discord_mention_factory, self.forum_thread_data_storage)

