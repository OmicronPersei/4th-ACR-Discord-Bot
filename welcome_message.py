import re

class WelcomeMessage:
    
    def __init__(self, config, discord_service, discord_mention_service):
        self._config = config
        self._discord = discord_service
        self._discord_mention_service = discord_mention_service

        self._discord.on_member_join_callbacks.append(self.member_joined)

    async def member_joined(self, user):
        messageToSend = self._config["message"]
        destinationChannel = self._config["channel"]

        messageToSend = messageToSend.replace("{joined_user}", "{user:0}")

        messageToSend = self._discord_mention_service.perform_replacement(messageToSend, [user])

        await self._discord.send_channel_message(messageToSend, destinationChannel)

    
