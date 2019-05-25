from discord_service import DiscordService
from welcome_message import WelcomeMessage
from discord_mention_factory import DiscordMentionFactory
from user_leave_notification import UserLeaveNotification
import json

def readJsonFile(file_name):
    with open(file_name, mode="r") as f:
        return json.load(f)

def read_config():
    return readJsonFile("config.json")

def read_secrets():
    return readJsonFile("secrets.json")


if __name__ == "__main__":
    config = read_config()

    secrets = read_secrets()
    discord_token = secrets["discord-bot-token"]
    
    discord_service = DiscordService()

    discord_mention_factory = DiscordMentionFactory(discord_service)

    welcome_message_config = config["welcome_message"]
    if welcome_message_config["enabled"]:
        welcome_message = WelcomeMessage(welcome_message_config, discord_service, discord_mention_factory)

    user_leave_config = config["user_leave_notification"]
    if user_leave_config["enabled"]:
        user_leave_notification = UserLeaveNotification(user_leave_config, discord_service, discord_mention_factory)

    discord_service.run(discord_token)

    