# map a discord.py Message object to the dict shape of
# user_id (key): { "user": userobj, "emojis": [emojis] }
async def map_message_to_user_reaction_dict(message):
    user_reaction_dict = dict()
    for reaction in message.reactions:
        emoji = reaction.emoji
        async for user in reaction.users():
            usr_id_str = str(user.id)
            if usr_id_str not in user_reaction_dict:
                user_reaction_dict[usr_id_str] = { "user": user, "emojis": [emoji] }
            else:
                user_reaction_dict[usr_id_str]["emojis"].append(emoji)
    return user_reaction_dict
        
