import discord
import inspect

class DiscordService(discord.Client):
    def __init__(self):
        super().__init__()
        self.on_member_join_callbacks = []
        self.on_member_remove_callbacks = []
        self.bot_command_callbacks = dict()

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

    def get_all_roles(self):
        return self.guilds[0].roles

    def create_listener_for_bot_command(self, command_prefix, callback):
        self.bot_command_callbacks[command_prefix.lower()] = callback

    async def on_message(self, message):
        tokens = message.content.split(" ")
        first_token = tokens[0].lower()
        if first_token in self.bot_command_callbacks:
            callback = self.bot_command_callbacks[first_token]
            if inspect.iscoroutinefunction(callback):
                await callback(message)
            else:
                callback(message)
                
                