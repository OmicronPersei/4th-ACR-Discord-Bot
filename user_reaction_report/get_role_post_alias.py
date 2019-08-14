def get_role_post_alias(role_id, config):
    aliases = config["role_aliases"]
    role_id = str(role_id)
    if role_id in aliases:
        return int(aliases[role_id])
    return int(role_id)