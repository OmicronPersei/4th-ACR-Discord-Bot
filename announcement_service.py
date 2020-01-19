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
        elif command.lower() == 'set-reactions':
            await self.set_reactions(message)

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

    async def set_reactions(self, message):
        msg_tokens = message.content.split(' ')
        channel = msg_tokens[2]
        msg_id = int(msg_tokens[3])
        new_reactions = set(msg_tokens[4:])

        msg_to_edit = await self.discord_service.get_matching_message(channel, msg_id)
        current_reactions = set([x.emoji for x in msg_to_edit.reactions])

        # remove any reactions no longer necessary
        for cur_reaction in current_reactions:
            if cur_reaction not in new_reactions:
                reaction_to_remove = [x for x in msg_to_edit.reactions if x.emoji == cur_reaction][0]
                async for user in reaction_to_remove.users:
                    await msg_to_edit.remove_reaction(cur_reaction, user)
        
        # add new reactions
        for new_reaction in new_reactions:
            if new_reaction not in current_reactions:
                await msg_to_edit.add_reaction(new_reaction)

    def user_has_allowed_role(self, message):
        allowed_roles = set(self.config.get(service_name)["allowed_roles"])
        for role in message.author.roles:
            if role.id in allowed_roles:
                return True
        return False
