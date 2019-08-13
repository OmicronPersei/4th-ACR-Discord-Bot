class BotCommandServiceBase:
    def __init__(self, config, service_name, discord_service):
        command_prefix = config.get(service_name)["command_keyword"]
        discord_service.create_listener_for_bot_command(command_prefix, self.bot_command_callback)
        self.config = config
        self.discord_service = discord_service

    def bot_command_callback(self, message):
        pass