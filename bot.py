from discord_service import DiscordService
from welcome_message import WelcomeMessage
from discord_mention_factory import DiscordMentionFactory
from user_leave_notification import UserLeaveNotification

from dependency_injection import Dependencies
import json
import asyncio

def readJsonFile(file_name):
    with open(file_name, mode="r") as f:
        return json.load(f)

def read_secrets():
    return readJsonFile("secrets.json")

def read_config():
    return readJsonFile("config.json")

def setup_dependency_injection(config, secrets):
    return Dependencies(config, secrets)

def start_bot(services, discord_token):
    discord_service = services.discord_service()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(discord_service.start(discord_token))
    except KeyboardInterrupt:
        handle_KeyboardInterrupt(discord_service, loop)

def handle_KeyboardInterrupt(discord_service, loop):
    print("Received keyboard interrupt, stopping services...")
    loop.run_until_complete(discord_service.logout())
    print("Logged out.")
    loop.close()

if __name__ == "__main__":
    config = read_config()
    secrets = read_secrets()
    discord_token = secrets["discord-bot-token"]

    services = setup_dependency_injection(config, secrets)

    if config["welcome_message"]["enabled"]:
        services.welcome_message()

    if config["user_leave_notification"]["enabled"]:
        services.user_leave_notification()

    start_bot(services, discord_token)
    