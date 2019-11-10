from bot_command_service_base import BotCommandServiceBase

class AnnouncementService(BotCommandServiceBase):
    def __init__(self, config, discord_service):
        super().__init__(config, "announcement_service", discord_service)