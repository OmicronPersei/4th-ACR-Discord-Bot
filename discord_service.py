import discord

class DiscordService(discord.Client):
    def __init__(self):
        super().__init__()
        self.on_member_join_callbacks = []
        self.on_member_remove_callbacks = []

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
        return [x for x in all_roles if x.name == role_name][0]