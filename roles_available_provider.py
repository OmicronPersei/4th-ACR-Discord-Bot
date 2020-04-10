from user_roles_hierarchy_parser import create_roles_dictionary

class RolesAvailableProvider:
    def __init__(self, user_roles_hierarchy_parser, discord_service, config_service):
        self.user_roles_hierarchy_parser = user_roles_hierarchy_parser
        self.discord_service = discord_service
        self.config_service = config_service

    def get_roles_for_channel(self, message):
        config = self.config_service.get("user_role_self_service")
        chan_id = message.channel.id
        roles_for_channels = self.user_roles_hierarchy_parser(config["available_roles"], config["main_request_channel"])
        roles_for_channel = roles_for_channels[str(chan_id)]

        return [self.discord_service.get_role_by_id(int(x)) for x in roles_for_channel]
