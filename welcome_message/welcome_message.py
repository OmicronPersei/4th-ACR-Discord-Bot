class welcome_message:
    def __init__(self, config, discord):
        self._config = config
        self._discord = discord

        self._discord.on_member_join_callbacks.append(self.member_joined)


    def member_joined(self, user):
        pass
    
    