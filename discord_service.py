import discord

class DiscordService(discord.Client):
    def __init__(self):
        super().__init__()
        self.on_member_join_callbacks = []
        self.on_member_remove_callbacks = []
        self.bot_command_callbacks = []

    async def on_member_join(self, member):
        for callback in self.on_member_join_callbacks:
            await callback(member)

    async def on_member_remove(self, member):
        for callback in self.on_member_remove_callbacks:
            await callback(member)

    async def send_channel_message(self, message, channel_name):
        channels = self.get_all_channels()
        channel = [x for x in channels if x.name == channel_name][0]
        await channel.send(message)

    def get_matching_Member(self, username, discriminator):
        all_members = self.get_all_members()

        matching_member = [x for x in all_members if x.name == username and x.discriminator == discriminator][0]
        return matching_member

    def get_matching_role(self, role_name):
        all_roles = self.guilds[0].roles
        return [x for x in all_roles if x.name.lower() == role_name.lower()][0]

    def get_all_roles_names(self):
        return [x.name for x in self.guilds[0].roles]

    def create_listener_for_bot_command(self, command_prefix, callback):
        self.bot_command_callbacks.append({ 
            "prefix": command_prefix, 
            "callback": callback
            })

    async def on_message(self, message):
        for bot_command_callback in self.bot_command_callbacks:
            if message.content.startswith(bot_command_callback["prefix"]):
                await bot_command_callback["callback"](message)