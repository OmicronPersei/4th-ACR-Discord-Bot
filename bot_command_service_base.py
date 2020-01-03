from configuration_service import ConfigurationService
from discord_service import DiscordService

class BotCommandServiceBase:
    def __init__(self, config: ConfigurationService, service_name: str, discord_service: DiscordService):
        command_prefix = config.get(service_name)["command_keyword"]
        discord_service.create_listener_for_bot_command(command_prefix, self.bot_command_callback)
        self.config = config
        self.discord_service = discord_service

    def bot_command_callback(self, message):
        pass