from bot_command_service_base import BotCommandServiceBase

from user_reaction_report.user_reaction_mapper import map_message_to_user_reaction_dict
from user_reaction_report.get_role_post_alias import get_role_post_alias
from user_reaction_report.get_matching_role_node import get_matching_role_node
from user_reaction_report.create_reaction_tree import create_reaction_tree
from user_reaction_report.serialize_reaction_tree import serialize_reaction_tree

service_name = "user_reaction_reporter"

class UserReactionReport(BotCommandServiceBase):
    def __init__(self, discord_service, config):
        super().__init__(config, service_name, discord_service)

    async def bot_command_callback(self, message):
        if self.should_ignore_this_msg(message):
            return

        config = self.config.get(service_name)
        
        tokens = message.content.split(" ")
        channel_msg_pair = tokens[1].split(":")
        channel_name = channel_msg_pair[0]
        msg_id = channel_msg_pair[1]
        target_role = " ".join(tokens[2:])
        
        target_message = await self.discord_service.get_matching_message(channel_name, int(msg_id))

        user_reaction_dict = await map_message_to_user_reaction_dict(target_message)

        role_id = self.discord_service.get_matching_role(target_role).id
        
        target_role_id = get_role_post_alias(role_id, config)
        role_node = get_matching_role_node(target_role_id, config["role_structure"])
        all_members = self.discord_service.get_all_members()
        reaction_tree = create_reaction_tree(role_node, all_members, user_reaction_dict)
        all_roles = self.discord_service.get_all_roles()
        serialized = serialize_reaction_tree(reaction_tree, config["emojis"], all_roles)
        result_channel = self.config.get(service_name)["restrict_to_channel"]
        self.discord_service.send_channel_message(serialized, result_channel)

    def should_ignore_this_msg(self, message):
        return self.config.get(service_name)["restrict_to_channel"].lower() != message.channel.name.lower()