from dependency_injector import providers

from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory
from user_leave_notification import UserLeaveNotification
from welcome_message import WelcomeMessage
from user_roles_service import UserRolesService

class Dependencies:
    def __init__(self, config):
        super().__init__()
        self.config = providers.Configuration("config")
        self.config.override(config)

        self.discord_service = providers.Singleton(DiscordService)
        self.discord_mention_factory = providers.Singleton(DiscordMentionFactory, self.discord_service)
        self.welcome_message = providers.Singleton(WelcomeMessage, self.config.welcome_message, self.discord_service, self.discord_mention_factory)
        self.user_leave_notification = providers.Singleton(UserLeaveNotification, self.config.user_leave_notification, self.discord_service, self.discord_mention_factory)
        self.user_roles_service = providers.Singleton(UserRolesService, self.config.user_role_self_service, self.discord_service)

