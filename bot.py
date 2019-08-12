from discord_service import DiscordService
from welcome_message import WelcomeMessage
from discord_mention_factory import DiscordMentionFactory
from user_leave_notification import UserLeaveNotification

from dependency_injection import Dependencies
import json

def readJsonFile(file_name):
    with open(file_name, mode="r") as f:
        return json.load(f)

def read_secrets():
    return readJsonFile("secrets.json")

def setup_dependency_injection(config):
    return Dependencies(config)

if __name__ == "__main__":
    secrets = read_secrets()
    discord_token = secrets["discord-bot-token"]

    services = setup_dependency_injection("config.json")
    config_service = services.config()
    
    if config_service.get("welcome_message").enabled:
        services.welcome_message()

    if config_service.get("user_leave_notification").enabled:
        services.user_leave_notification()

    if config_service.get("user_role_self_service").enabled:
        services.user_roles_service()

    discord_service = services.discord_service()
    discord_service.run(discord_token)