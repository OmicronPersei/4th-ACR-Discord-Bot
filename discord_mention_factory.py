import re

class DiscordMentionFactory:
    def __init__(self, discord_service):
        self._discord = discord_service

    def perform_replacement(self, template, user_objs=None):
        template = self._perform_member_replacement(template)
        if user_objs is not None:
            template = self._perform_user_mention_replacement(template, user_objs)
            template = self._perform_user_display_name_replacement(template, user_objs)
        template = self._perform_role_replacement(template)
        return template

    def _perform_member_replacement(self, message):
        member_matches = self._get_member_strings(message)
        member_replace_dict = dict()
        for member in member_matches:
            if member not in member_replace_dict:
                username,discriminator = member[8:-1].split("#")
                memberObj = self._discord.get_matching_Member(username, discriminator)
                member_replace_dict[member] = memberObj.mention
        
        for (key,value) in member_replace_dict.items():
            message = message.replace(key, value)

        return message

    def _perform_user_mention_replacement(self, message, user_objs):
        for i,user in enumerate(user_objs, 0):
            replace = "{user:" + str(i) + "}"
            message = message.replace(replace, user.mention)
        return message

    def _perform_user_display_name_replacement(self, message, user_objs):
        for i,user in enumerate(user_objs, 0):
            replace = "{user:display_name:" + str(i) + "}"
            message = message.replace(replace, user.display_name)
        return message
    
    def _perform_role_replacement(self, message):
        roles_mentioned = set(self._get_role_strings(message))
        roles_replace_dict = dict()
        for role in roles_mentioned:
            if role not in roles_replace_dict:
                role_name = role[6:-1]
                role_obj = self._discord.get_matching_role(role_name)
                roles_replace_dict[role]=role_obj.mention

        for key,value in roles_replace_dict.items():
            message = message.replace(key, value)
        
        return message

    def _get_role_strings(self, message):
        matches_for_replacement = self._get_replacable_items(message)
        return [x for x in matches_for_replacement if x.startswith("{role:")]

    def _get_member_strings(self, message):
        matches_for_replacement = self._get_replacable_items(message)
        return [x for x in matches_for_replacement if x.startswith("{member:")]

    def _get_replacable_items(self, message):
        return set(re.findall(r"\{[^\{\}]*}", message))

    