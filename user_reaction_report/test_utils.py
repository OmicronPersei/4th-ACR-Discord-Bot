from unittest.mock import MagicMock, PropertyMock

def create_mock_user(mention_val="some_val", display_name_val="stub_name_here", id=2343243, roles=None):
    mock_user = MagicMock()
    type(mock_user).mention = PropertyMock(return_value=mention_val)
    type(mock_user).display_name = PropertyMock(return_value=display_name_val)
    type(mock_user).id = PropertyMock(return_value=id)
    type(mock_user).roles = PropertyMock(return_value=roles)
    return mock_user

def create_mock_role(id, name):
    role = MagicMock()
    type(role).id = PropertyMock(return_value=int(id))
    type(role).name = PropertyMock(return_value=name)
    return role