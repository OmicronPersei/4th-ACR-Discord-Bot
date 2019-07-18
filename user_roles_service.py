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
        available_role_strs = ["`{}`".format(x) for x in self.get_available_roles()]
        response = "Roles available:\n{}".format("\n".join(available_role_strs))
        destination_channel = message.channel.name
        await self.discord_service.send_channel_message(response, destination_channel)

    def get_available_roles(self):
        blacklisted_roles = list_lower(self.config["blacklisted_roles"])
        all_roles = self.discord_service.get_all_roles_names()
        return [x for x in all_roles if x.lower() not in blacklisted_roles]

    async def handle_add_role(self, message):
        role_name = get_role_name_from_command(message)

        if role_name not in list_lower(self.get_available_roles()):
            return

        new_roles = message.author.roles[:]

        if role_name in [x.name.lower() for x in new_roles]:
            return

        matching_new_role = self.discord_service.get_matching_role(role_name)
        new_roles.append(matching_new_role)
        await message.author.edit(roles=new_roles)

    async def handle_remove_role(self, message):
        role_name = get_role_name_from_command(message)

        if role_name not in list_lower(self.get_available_roles()):
            return

        if role_name not in [x.name.lower() for x in message.author.roles]:
            return
        
        new_roles = [x for x in message.author.roles if x.name.lower() != role_name]

        await message.author.edit(roles=new_roles)


def list_lower(items):
    return [x.lower() for x in items]

def get_role_name_from_command(message):
    return " ".join(message.content.split(" ")[2:]).lower()