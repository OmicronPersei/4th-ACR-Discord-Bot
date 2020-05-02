class RolesAvailableProvider:
    def __init__(self, discord_service, config_service):
        self.discord_service = discord_service
        self.config_service = config_service

    def get_roles_for_message(self, message):
        config = self.config_service.get("user_role_self_service")
        chan_id = message.channel.id
        try:
            roles_for_channel = config["channels_available_roles"][str(chan_id)]

            return [self.discord_service.get_role_by_id(int(x)) for x in roles_for_channel]
        except KeyError:
            return []
