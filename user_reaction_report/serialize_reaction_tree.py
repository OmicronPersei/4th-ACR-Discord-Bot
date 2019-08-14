indent_str = "     "

def serialize_reaction_tree(reaction_tree, emoji_templates, all_roles):
    roles_dict = dict()
    for role in all_roles:
        roles_dict[str(role.id)] = role
    return "\n".join(serialize_nodes(reaction_tree, emoji_templates, roles_dict))

def serialize_nodes(reaction_tree, emoji_templates, roles_dict):
    buffer = []
    role_name = roles_dict[reaction_tree["role_id"]].name
    for reaction in reaction_tree["reactions"]:
        template = emoji_templates[reaction["emoji"]]["display_template"]
        serialized = template.format(user=reaction["user"].display_name, role=role_name)
        buffer.append(serialized)
    if "children" in reaction_tree:
        for child in reaction_tree["children"]:
            serialized = serialize_nodes(child, emoji_templates, roles_dict)
            for s in serialized:
                buffer.append(indent_str + s)
    return buffer
            