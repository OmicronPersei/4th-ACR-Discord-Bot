async def map_message_to_user_reaction_dict(message):
    username_reaction_dict = dict()
    for reaction in message.reactions:
        emoji = reaction.emoji
        async for user in reaction.users():
            username = (user.name + "#" + user.discriminator).lower()
            if username not in username_reaction_dict:
                username_reaction_dict[username] = [emoji]
            else:
                username_reaction_dict[username].append(emoji)
    return username_reaction_dict
        
