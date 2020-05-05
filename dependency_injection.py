from dependency_injector import providers

from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory
from user_leave_notification import UserLeaveNotification
from welcome_message import WelcomeMessage
from user_roles_service import UserRolesService
from cached_configuration_service import CachedConfigurationService
from user_reaction_report.user_reaction_report import UserReactionReport
from announcement_service import AnnouncementService
from roles_available_provider import RolesAvailableProvider

class Dependencies:
    def __init__(self, config_path):
        super().__init__()

        self.config = self._create_config_service(config_path)
        self.discord_service = providers.Singleton(DiscordService)
        self.discord_mention_factory = providers.Singleton(DiscordMentionFactory, self.discord_service)
        self.welcome_message = providers.Singleton(WelcomeMessage, self.config, self.discord_service, self.discord_mention_factory)
        self.user_leave_notification = providers.Singleton(UserLeaveNotification, self.config, self.discord_service, self.discord_mention_factory)
        self.roles_available_provider = providers.Singleton(RolesAvailableProvider, self.discord_service, self.config)
        self.user_roles_service = providers.Singleton(UserRolesService, self.config, self.discord_service, self.roles_available_provider)
        self.user_reaction_report = providers.Singleton(UserReactionReport, self.discord_service, self.config)
        self.announcement_service = providers.Singleton(AnnouncementService, self.config, self.discord_service)

    def _create_config_service(self, config_path):
        return providers.Singleton(CachedConfigurationService, config_path)

