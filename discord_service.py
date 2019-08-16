import discord
import inspect

class DiscordService(discord.Client):
    def __init__(self):
        super().__init__()
        self.on_member_join_callbacks = []
        self.on_member_remove_callbacks = []
        self.bot_command_callbacks = dict()
        self.channel_dict = dict()

    async def on_ready(self):
        self._populate_channel_dict()
        print("bot is ready")

    def _populate_channel_dict(self):
        channels = self.get_all_channels()
        for channel in channels:
            self.channel_dict[channel.name.lower()] = channel.id

    def _get_channel_id(self, name):
        name_lower = name.lower()
        if name_lower in self.channel_dict:
            return self.channel_dict[name_lower]

        #Cache miss.  Find then enter it into the cache
        for channel in self.get_all_channels():
            if channel.name.lower() == name_lower:
                self.channel_dict[name_lower] = channel.id
                return channel.id

    async def on_member_join(self, member):
        for callback in self.on_member_join_callbacks:
            await callback(member)

    async def on_member_remove(self, member):
        for callback in self.on_member_remove_callbacks:
            await callback(member)

    async def send_channel_message(self, message, channel_name):
        channel = self.get_channel(channel_name)
        await channel.send(message)

    def get_channel(self, channel_name):
        chan_id = self._get_channel_id(channel_name)
        return super().get_channel(chan_id)

    def get_matching_Member(self, username, discriminator):
        all_members = self.get_all_members()
        for member in all_members:
            if member.name == username and member.discriminator == discriminator:
                return member

    def get_matching_role(self, role_name):
        all_roles = self.guilds[0].roles
        role_name_lower = role_name.lower()
        for role in all_roles:
            if role.name.lower() == role_name_lower:
                return role

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

    async def get_matching_message(self, target_channel, message_id):
        channel = self.get_channel(target_channel)
        async for m in channel.history(limit=100):
            if m.id == message_id:
                return m
                
                