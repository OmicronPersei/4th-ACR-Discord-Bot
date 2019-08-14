def create_reaction_tree(structure, all_users, reaction_dict):
    return traverse(structure, {}, all_users, reaction_dict)

def traverse(structure, reaction_tree, all_users, reaction_dict):
    role_id = structure["role_id"]
    users_in_role = get_users_in_role(all_users, role_id)    
    reactions = []
    for user in users_in_role:
        user_id = str(user.id)
        if user_id in reaction_dict and len(reaction_dict[user_id]["emojis"]) == 1:
            emoji = reaction_dict[user_id]["emojis"][0]
            reactions.append({ "user": user, "emoji":  emoji})
        elif user_id not in reaction_dict:
            emoji = ""
            reactions.append({ "user": user, "emoji":  emoji})
        
    reaction_tree["role_id"] = role_id
    reaction_tree["reactions"] = reactions

    if "children" in structure:
        children = []
        for child in structure["children"]:
            node = traverse(child, {}, all_users, reaction_dict)
            children.append(node)
        reaction_tree["children"] = children
    
    return reaction_tree

def get_users_in_role(all_users, role_id):
    return [u for u in all_users if len([r for r in u.roles if r.id == int(role_id)]) > 0]