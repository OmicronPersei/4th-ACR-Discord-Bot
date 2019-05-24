import re

class WelcomeMessage:
    
    def __init__(self, config, discord_service):
        self._config = config
        self._discord = discord_service

        self._discord.on_member_join_callbacks.append(self.member_joined)

    async def member_joined(self, user):
        messageToSend = self._config["message"]
        destinationChannel = self._config["channel"]

        messageToSend = self.perform_member_replacement(messageToSend)
        messageToSend = self.perform_joined_user_replacement(messageToSend, user)
        messageToSend = self.perform_role_replacement(messageToSend)

        await self._discord.send_channel_message(messageToSend, destinationChannel)

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

    def perform_joined_user_replacement(self, message, joined_user):
        return message.replace("{joined_user}", joined_user.mention)
    
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

    def get_role_strings(self, message):
        matches_for_replacement = self.get_replacable_items(message)
        return [x for x in matches_for_replacement if x.startswith("{role:")]

    def get_replacable_items(self, message):
        return set(re.findall(r"\{[^\{\}]*}", message))

    def get_member_strings(self, message):
        matches_for_replacement = self.get_replacable_items(message)
        return [x for x in matches_for_replacement if x.startswith("{member:")]
