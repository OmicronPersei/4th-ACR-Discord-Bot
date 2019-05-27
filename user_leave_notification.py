class UserLeaveNotification:
    def __init__(self, config, discord_service, discord_mention_factory):
        self._config = config
        self._discord = discord_service
        self._discord.on_member_remove_callbacks.append(self._user_leave_callback)
        self._discord_mention_factory = discord_mention_factory

    async def _user_leave_callback(self, user):
        message = self._config["message"]
        channel = self._config["channel"]
        
        message = message.replace("{left_user}", "{user:display_name:0}")
        message = self._discord_mention_factory.perform_replacement(message, [user])

        await self._discord.send_channel_message(message, channel)