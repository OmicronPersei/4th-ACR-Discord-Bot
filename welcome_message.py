class WelcomeMessage:
    def __init__(self, config, discord_service):
        self._config = config
        self._discord = discord_service

        self._discord.on_member_join_callbacks.append(self.member_joined)


    def member_joined(self, user):
        messageToSend = self._config["message"]
        destinationChannel = self._config["channel"]

        self._discord.send_channel_message(message=messageToSend, channel=destinationChannel)
    
    