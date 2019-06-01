import dependency_injector
import asynctest

from dependency_injection import Dependencies
from discord_service import DiscordService
from discord_mention_factory import DiscordMentionFactory
from welcome_message import WelcomeMessage
from user_leave_notification import UserLeaveNotification
from forum_thread_data_storage import ForumThreadDataStorage
from sql_wrapper import SQLWrapper
from xen_foro_request_factory import XenForoRequestFactory
from xen_foro_thread_getter import XenForoThreadGetter
from xen_foro_new_thread_detector import XenForoNewThreadDetector

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
        "db_filename": ":memory:"
    }

def create_mock_secrets():
    return {
        "xen_foro_integration_api_token": "imsecret"
    }

class TestDependenciesSetsConfigAndSecrets(asynctest.TestCase):
    def setUp(self):
        self.config = create_mock_config()
        self.secrets = create_mock_secrets()
    
    def runTest(self):
        dependencies = Dependencies(self.config, self.secrets)
        assert dependencies.config.welcome_message.enabled() == True
        assert dependencies.secrets.xen_foro_integration_api_token() == "imsecret"

class TestDependenciesSetsupDependencies(asynctest.TestCase):
    def setUp(self):
        self.config = create_mock_config()
        self.secrets = create_mock_secrets()
        self.dependencies = Dependencies(self.config, self.secrets)
    
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

        sql_wrapper = self.dependencies.sql_wrapper
        sql_wrapper_instance = self.dependencies.sql_wrapper()
        assert isinstance(sql_wrapper, dependency_injector.providers.Singleton)
        assert isinstance(sql_wrapper_instance, SQLWrapper)

        forum_thread_data_storage = self.dependencies.forum_thread_data_storage
        forum_thread_data_storage_instance = self.dependencies.forum_thread_data_storage()
        assert isinstance(forum_thread_data_storage, dependency_injector.providers.Singleton)
        assert isinstance(forum_thread_data_storage_instance, ForumThreadDataStorage)

        xen_foro_request_factory = self.dependencies.xen_foro_request_factory
        xen_foro_request_factory_instance = self.dependencies.xen_foro_request_factory()
        assert isinstance(xen_foro_request_factory, dependency_injector.providers.Singleton)
        assert isinstance(xen_foro_request_factory_instance, XenForoRequestFactory)

        xen_foro_thread_getter = self.dependencies.xen_foro_thread_getter
        xen_foro_thread_getter_instance = self.dependencies.xen_foro_thread_getter()
        assert isinstance(xen_foro_thread_getter, dependency_injector.providers.Singleton)
        assert isinstance(xen_foro_thread_getter_instance, XenForoThreadGetter)

        xen_foro_new_thread_detector = self.dependencies.xen_foro_new_thread_detector
        xen_foro_new_thread_detector_instance = self.dependencies.xen_foro_new_thread_detector()
        assert isinstance(xen_foro_new_thread_detector, dependency_injector.providers.Singleton)
        assert isinstance(xen_foro_new_thread_detector_instance, XenForoNewThreadDetector)

    