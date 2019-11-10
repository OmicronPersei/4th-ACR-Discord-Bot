from bot_command_service_base import BotCommandServiceBase

class AnnouncementService(BotCommandServiceBase):
    def __init__(self, config, discord_service):
        super().__init__(config, "announcement_service", discord_service)

    async def bot_command_callback(self, message):
        msg_tokens = message.split(' ')
        channel = msg_tokens[1]
        announcement = ' '.join(msg_tokens[2:])

        await self.discord_service.send_channel_message(announcement, channel)
