from bot_command_service_base import BotCommandServiceBase

service_name = "announcement_service"

class AnnouncementService(BotCommandServiceBase):
    def __init__(self, config, discord_service):
        super().__init__(config, service_name, discord_service)

    async def bot_command_callback(self, message):
        if not self.user_has_allowed_role(message):
            return

        msg_tokens = message.content.split(' ')
        channel = msg_tokens[1]
        announcement = ' '.join(msg_tokens[2:])

        await self.discord_service.send_channel_message(announcement, channel)

    def user_has_allowed_role(self, message):
        allowed_roles = set(self.config.get(service_name)["allowed_roles"])
        for role in message.author.roles:
            if role.id in allowed_roles:
                return True
        return False
