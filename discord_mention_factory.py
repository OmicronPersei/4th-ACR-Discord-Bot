import re

class DiscordMentionFactory:
    def __init__(self, discord_service):
        self._discord = discord_service

    def perform_replacement(self, template, user_objs=None):
        template = self.perform_member_replacement(template)
        if user_objs is not None:
            template = self.perform_user_mention_replacement(template, user_objs)
            template = self.perform_user_display_name_replacement(template, user_objs)
        template = self.perform_role_replacement(template)
        template = self.perform_channel_replacement(template)
        return template

    def perform_member_replacement(self, message):
        member_matches = self.get_member_strings(message)
        member_replace_dict = dict()
        for member in member_matches:
            if member not in member_replace_dict:
                # eg: `{member:Exe#123}`
                username,discriminator = member[8:-1].split("#")
                memberObj = self._discord.get_matching_Member(username, discriminator)
                member_replace_dict[member] = memberObj.mention
        
        for (key,value) in member_replace_dict.items():
            message = message.replace(key, value)

        return message

    def perform_user_mention_replacement(self, message, user_objs):
        for i,user in enumerate(user_objs, 0):
            replace = "{user:" + str(i) + "}"
            message = message.replace(replace, user.mention)
        return message

    def perform_user_display_name_replacement(self, message, user_objs):
        for i,user in enumerate(user_objs, 0):
            replace = "{user:display_name:" + str(i) + "}"
            message = message.replace(replace, user.display_name)
        return message
    
    def perform_role_replacement(self, message):
        roles_mentioned = set(self.get_role_strings(message))
        roles_replace_dict = dict()
        for role in roles_mentioned:
            if role not in roles_replace_dict:
                # eg: `{role:Recruiter}`
                role_name = role[6:-1]
                role_obj = self._discord.get_matching_role(role_name)
                roles_replace_dict[role]=role_obj.mention

        for key,value in roles_replace_dict.items():
            message = message.replace(key, value)
        
        return message

    def perform_channel_replacement(self, message):
        channels_mentioned = set(self.get_channel_strings(message))
        channel_mention_dict = dict()

        for channel_mention in channels_mentioned:
            #eg: `{channel:thechannel}`
            channel_name = channel_mention[9:-1]
            channel_obj = self._discord.get_channel(channel_name)
            channel_mention_dict[channel_mention] = channel_obj.mention
        
        for key,value in channel_mention_dict.items():
            message = message.replace(key, value)
        
        return message

    def get_role_strings(self, message):
        return self.get_replacable_items_with_prefix("role", message)

    def get_member_strings(self, message):
        return self.get_replacable_items_with_prefix("member", message)

    def get_channel_strings(self, message):
        return self.get_replacable_items_with_prefix("channel", message)

    def get_replacable_items_with_prefix(self, prefix, message):
        replacable_items = self.get_replacable_items(message)
        formatted_prefix = '{' + prefix + ':'
        return [x for x in replacable_items if x.startswith(formatted_prefix)]

    def get_replacable_items(self, message):
        return set(re.findall(r"\{[^\{\}]*}", message))
    