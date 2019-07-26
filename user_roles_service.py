from bot_command_service_base import BotCommandServiceBase

class UserRolesService(BotCommandServiceBase):
    def __init__(self, config, discord_service):
        super().__init__(config, discord_service)

    async def bot_command_callback(self, message):
        command_tokens = message.content.split(" ")

        if self.should_ignore_command(message):
            return

        if len(command_tokens) == 1:
            await self.reply_with_all_roles(message)
        elif command_tokens[1].lower() == "add":
            await self.handle_add_role(message)
        elif command_tokens[1].lower() == "remove":
            await self.handle_remove_role(message)

        await message.delete()

    def should_ignore_command(self, message):
        return ("restrict_to_channel" in self.config and
            self.config["restrict_to_channel"] != None and
            message.channel.name.lower() != self.config["restrict_to_channel"].lower())

    async def reply_with_all_roles(self, message):
        available_role_strs = ["`{}`".format(x.name) for x in self.get_available_roles()]
        response = "Roles available:\n{}".format("\n".join(available_role_strs))
        destination_channel = message.channel.name
        await self.discord_service.send_channel_message(response, destination_channel)

    async def handle_add_role(self, message):
        role_name = get_role_name_from_command(message)
        try:
            new_role = self.get_role_obj_from_name(role_name)
        except:
            # Role name didn't resolve to an existing role object, return
            return

        if new_role.id not in [x.id for x in self.get_available_roles()]:
            # Role is not available for self assignment, return
            return

        new_roles = message.author.roles[:]

        if new_role.id in [x.id for x in new_roles]:
            # User already has this role, return
            return

        new_roles.append(new_role)
        await message.author.edit(roles=new_roles)

    async def handle_remove_role(self, message):
        role_name = get_role_name_from_command(message)
        try:
            matching_role_obj = self.get_role_obj_from_name(role_name)
        except:
            # Role name didn't resolve to an existing role object, return
            return

        if matching_role_obj.id not in [x.id for x in self.get_available_roles()]:
            # Role is not available for self assignment, return
            return

        if matching_role_obj.id not in [x.id for x in message.author.roles]:
            # User doesn't have this role, return
            return        
        
        new_roles = [x for x in message.author.roles if x.id != matching_role_obj.id]

        await message.author.edit(roles=new_roles)

    def get_available_roles(self):
        blacklisted_roles = self.config["blacklisted_roles"]
        all_roles = self.discord_service.get_all_roles()
        return [x for x in all_roles if x.id not in blacklisted_roles]

    def get_role_obj_from_name(self, name):
        roles = self.get_available_roles()
        return [x for x in roles if x.name.lower() == name.lower()][0]

def get_role_name_from_command(message):
    return " ".join(message.content.split(" ")[2:]).lower()