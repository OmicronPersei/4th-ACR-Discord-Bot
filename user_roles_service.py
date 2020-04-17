from bot_command_service_base import BotCommandServiceBase

config_key = "user_role_self_service"

class UserRolesService(BotCommandServiceBase):
    def __init__(self, config, discord_service, roles_available_provider):
        super().__init__(config, config_key, discord_service)
        self.roles_available_provider = roles_available_provider

    async def bot_command_callback(self, message):
        command_tokens = message.content.split(" ")
        command_keyword = self.config.get(config_key)["command_keyword"]
        if self.should_ignore_command(command_tokens, command_keyword):
            return
        
        available_roles = self.roles_available_provider.get_roles_for_message(message)

        if self.does_not_has_available_roles_for_cmd(available_roles):
            await message.delete()
            return

        if len(command_tokens) == 1:
            await self.reply_with_roles_available(message, available_roles)
        elif command_tokens[1].lower() == "add":
            await self.handle_add_role(message, available_roles)
        elif command_tokens[1].lower() == "remove":
            await self.handle_remove_role(message, available_roles)

        await message.delete()

    def should_ignore_command(self, command_tokens, command_keyword):
        return command_tokens[0].lower() != command_keyword.lower()

    def does_not_has_available_roles_for_cmd(self, available_roles):
        return len(available_roles) == 0

    async def reply_with_roles_available(self, message, available_roles):
        available_role_strs = ["`{}`".format(x.name) for x in available_roles]
        response = "Roles available:\n{}".format("\n".join(available_role_strs))
        destination_channel_id = message.channel.id
        await self.discord_service.send_channel_message(response, channel_id=destination_channel_id)
        
    async def handle_add_role(self, message, available_roles):
        role_name = get_role_name_from_command(message)
        try:
            new_role = get_matching_role_obj(available_roles, role_name)
        except:
            # Role name didn't resolve to an available role object, return
            return

        new_roles = message.author.roles[:]

        if new_role.id in [x.id for x in new_roles]:
            # User already has this role, return
            return

        new_roles.append(new_role)
        await message.author.edit(roles=new_roles)

    

    async def handle_remove_role(self, message, available_roles):
        role_name = get_role_name_from_command(message)
        try:
            matching_role_obj = get_matching_role_obj(available_roles, role_name)
        except:
            # Role name didn't resolve to an existing role object, return
            return

        if matching_role_obj.id not in [x.id for x in message.author.roles]:
            # User doesn't have this role, return
            return        
        
        new_roles = [x for x in message.author.roles if x.id != matching_role_obj.id]

        await message.author.edit(roles=new_roles)

def get_role_name_from_command(message):
    return " ".join(message.content.split(" ")[2:]).lower()

def get_matching_role_obj(roles, role_name):
    return [x for x in roles if x.name.lower() == role_name][0]