import dependency_injector
from asynctest import TestCase

from dependency_injection import Dependencies
from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory
from welcome_message import WelcomeMessage
from user_leave_notification import UserLeaveNotification
from user_roles_service import UserRolesService
from cached_configuration_service import CachedConfigurationService

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

class TestBase:
    def setUp(self):
        self.dependencies = Dependencies(None)

class TestConfigurationServiceDependencyInjection(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)
    
    def runTest(self):
        config = self.dependencies.config
        config_instance = self.dependencies.config()
        assert isinstance(config, dependency_injector.providers.Singleton)
        assert isinstance(config_instance, CachedConfigurationService)

class TestDiscordServiceeDependencyInjection(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)
    
    def runTest(self):
        discord_service = self.dependencies.discord_service
        discord_service_instance = discord_service()
        assert isinstance(discord_service, dependency_injector.providers.Singleton)
        assert isinstance(discord_service_instance, DiscordService)

class TestDiscordMentionFactoryDependencyInjection(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)
    
    def runTest(self):
        discord_mention_factory = self.dependencies.discord_mention_factory
        discord_mention_factory_instance = discord_mention_factory()
        assert isinstance(discord_mention_factory, dependency_injector.providers.Singleton)
        assert isinstance(discord_mention_factory_instance, DiscordMentionFactory)

        
class TestWelcomeMessageDependencyInjection(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)
    
    def runTest(self):
        welcome_message = self.dependencies.welcome_message
        welcome_message_instance = welcome_message()
        assert isinstance(welcome_message, dependency_injector.providers.Singleton)
        assert isinstance(welcome_message_instance, WelcomeMessage)

class TestUserLeaveNotificationDependencyInjection(TestBase, TestCase):
    def setUp(self):
        TestBase.setUp(self)
    
    def runTest(self):
        user_leave_notification = self.dependencies.user_leave_notification
        user_leave_notification_instance = user_leave_notification()
        assert isinstance(user_leave_notification, dependency_injector.providers.Singleton)
        assert isinstance(user_leave_notification_instance, UserLeaveNotification)

class MockConfigService:
    def get(self, prop_key):
        return { "command_keyword": "!roles" }

class MockDependencies(Dependencies):
    def _create_config_service(self, config_path):
        return dependency_injector.providers.Singleton(MockConfigService)

class TestUserRolesServiceDependencyInjection(TestCase):
    def setUp(self):
        self.dependencies = MockDependencies(None)
    
    def runTest(self):
        user_roles_service = self.dependencies.user_roles_service
        user_roles_service_instance = user_roles_service()
        assert isinstance(user_roles_service, dependency_injector.providers.Singleton)
        assert isinstance(user_roles_service_instance, UserRolesService)
        

        
        
        

        

        

        