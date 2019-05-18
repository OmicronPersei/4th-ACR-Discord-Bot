from discord_service import DiscordService
from welcome_message import WelcomeMessage
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
    welcome_message = WelcomeMessage(config, discord_service)

    discord_service.run(discord_token)

    