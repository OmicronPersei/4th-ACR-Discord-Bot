import json
import asyncio

from discord_service import DiscordService
from dependency_injection import Dependencies

def readJsonFile(file_name):
    with open(file_name, mode="r") as f:
        return json.load(f)

def read_secrets():
    return readJsonFile("secrets.json")

def read_config():
    return readJsonFile("config.json")

def setup_dependency_injection(config, secrets):
    return Dependencies(config, secrets)

def start_bot(services, discord_token, config):
    discord_service = services.discord_service()
    loop = asyncio.get_event_loop()
    start_services(services, config)
    try:
        loop.run_until_complete(discord_service.start(discord_token))
    except KeyboardInterrupt:
        handle_KeyboardInterrupt(discord_service, loop)

def start_services(services, config):
    if config["welcome_message"]["enabled"]:
        services.welcome_message()

    if config["user_leave_notification"]["enabled"]:
        services.user_leave_notification()

    if config["user_role_self_service"]["enabled"]:
        services.user_roles_service()
    
    if config["xen_foro_integration"]["enabled"]:
        services.xen_foro_new_message_dispatcher()

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
    
    start_bot(services, discord_token, config)