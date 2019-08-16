def get_matching_role_node(role_id, structure):
    return _find_role(role_id, structure)

def _find_role(role_id, node):
    if isinstance(node, list):
        for child in node:
            result = _find_role(role_id, child)
            if result is not None:
                return result
    else:
        if node["role_id"] == role_id:
            return node

        if "children" in node:
            for child in node["children"]:
                result = _find_role(role_id, child)
                if result is not None:
                    return result

    return None