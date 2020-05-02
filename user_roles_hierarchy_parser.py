def create_roles_dictionary(roles: list, default_channel: str):
    channel_roles = dict()
    default_channel_roles = []
    for role in roles:
        if _has_role(role):
            default_channel_roles.append(role["role"])
        if _has_sub_roles(role):
            _recurse_channel_roles(channel_roles, role)
    channel_roles[default_channel] = default_channel_roles

    return channel_roles

def _recurse_channel_roles(channel_roles_dict: dict, node: object):
    cur_chan = node["sub_roles_access_channel"]
    roles = []
    for sub_role in node["sub_roles"]:
        if _has_role(sub_role):
            roles.append(sub_role["role"])
        if _has_sub_roles(sub_role):
            _recurse_channel_roles(channel_roles_dict, sub_role)
    channel_roles_dict[cur_chan] = roles

def _has_role(node: object):
    return "role" in node

def _has_sub_roles(node: object):
    return "sub_roles_access_channel" in node and "sub_roles" in node