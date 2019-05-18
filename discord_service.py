import discord

class DiscordService(discord.Client):
    def __init__(self):
        super().__init__(self)
        self.on_member_join_callbacks = []

    async def on_member_join(self, member):
        for callback in self.on_member_join_callbacks:
            callback(member)