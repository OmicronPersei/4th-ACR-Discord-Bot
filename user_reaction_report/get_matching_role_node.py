def get_matching_role_node(role_id, structure):
    return find_role(role_id, structure)

def find_role(role_id, node):
    if node["role_id"] == role_id:
        return node

    if node["children"]:
        for child in node["children"]:
            result = find_role(role_id, child)
            if result is not None:
                return result

    return None