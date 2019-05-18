import discord

class DiscordService(discord.Client):
    def __init__(self):
        super().__init__(self)
        self.on_member_join_callbacks = []

    def on_member_join(self, member):
        for callback in self.on_member_join_callbacks:
            callback(member)

    def send_channel_message(self, message, channel):
        pass

    def get_matching_Member(self, display_name):
        all_members = self.get_all_members()
        matching_member = [x for x in all_members if x.display_name == display_name][0]
        return matching_member