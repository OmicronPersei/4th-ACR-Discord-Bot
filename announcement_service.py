from bot_command_service_base import BotCommandServiceBase

service_name = "announcement_service"

class AnnouncementService(BotCommandServiceBase):
    def __init__(self, config, discord_service):
        super().__init__(config, service_name, discord_service)

    async def bot_command_callback(self, message):
        if not self.user_has_allowed_role(message):
            return

        msg_tokens = message.content.split(' ')
        command = msg_tokens[1]

        if command.lower() == 'create':
            await self.create_announcement(message)
        elif command.lower() == 'edit':
            await self.edit_announcement(message)

    async def create_announcement(self, message):
        msg_tokens = message.content.split(' ')
        channel = msg_tokens[2]
        announcement = ' '.join(msg_tokens[3:])
        await self.discord_service.send_channel_message(announcement, channel)

    async def edit_announcement(self, message):
        msg_tokens = message.content.split(' ')
        channel = msg_tokens[2]
        msg_id = int(msg_tokens[3])
        announcement = ' '.join(msg_tokens[4:])
        msg_to_edit = await self.discord_service.get_matching_message(channel, msg_id)
        await msg_to_edit.edit(content=announcement)

    def user_has_allowed_role(self, message):
        allowed_roles = set(self.config.get(service_name)["allowed_roles"])
        for role in message.author.roles:
            if role.id in allowed_roles:
                return True
        return False
