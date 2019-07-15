import dependency_injector
import asynctest

from dependency_injection import Dependencies
from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory
from welcome_message import WelcomeMessage
from user_leave_notification import UserLeaveNotification
from user_roles_service import UserRolesService

def create_mock_config():
    return {
        "welcome_message": {
            "message": "the message",
            "channel": "the channel",
            "enabled": True
        },
        "user_leave_notification": {
            "message": "the message",
            "channel": "the channel",
            "enabled": True
        },
        "user_role_self_service": {
            "blacklisted_roles": [ "admin" ],
            "command_keyword": "!roles"
        }
    }

class TestDependenciesSetsConfig(asynctest.TestCase):
    def setUp(self):
        self.config = create_mock_config()
    
    def runTest(self):
        dependencies = Dependencies(self.config)
        assert dependencies.config.welcome_message.enabled() == True

class TestDependenciesSetsupDependencies(asynctest.TestCase):
    def setUp(self):
        self.config = create_mock_config()
        self.dependencies = Dependencies(self.config)
    
    def runTest(self):
        discord_service = self.dependencies.discord_service
        discord_service_instance = discord_service()
        assert isinstance(discord_service, dependency_injector.providers.Singleton)
        assert isinstance(discord_service_instance, DiscordService)
        
        discord_mention_factory = self.dependencies.discord_mention_factory
        discord_mention_factory_instance = discord_mention_factory()
        assert isinstance(discord_mention_factory, dependency_injector.providers.Singleton)
        assert isinstance(discord_mention_factory_instance, DiscordMentionFactory)

        welcome_message = self.dependencies.welcome_message
        welcome_message_instance = welcome_message()
        assert isinstance(welcome_message, dependency_injector.providers.Singleton)
        assert isinstance(welcome_message_instance, WelcomeMessage)

        user_leave_notification = self.dependencies.user_leave_notification
        user_leave_notification_instance = user_leave_notification()
        assert isinstance(user_leave_notification, dependency_injector.providers.Singleton)
        assert isinstance(user_leave_notification_instance, UserLeaveNotification)

        user_roles_service = self.dependencies.user_roles_service
        user_roles_service_instance = user_roles_service()
        assert isinstance(user_roles_service, dependency_injector.providers.Singleton)
        assert isinstance(user_roles_service_instance, UserRolesService)