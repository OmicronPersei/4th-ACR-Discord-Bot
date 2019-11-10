from unittest.mock import MagicMock, PropertyMock
from asyncio import Future

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

def MockConfigurationService(config_obj):
    service = MagicMock()
    service.get = MagicMock()
    service.get.side_effect = lambda x: config_obj[x]
    return service

def create_mock_message(msg_content, channel_name, user_roles=None):
    mock_message = MagicMock()
    type(mock_message).content = PropertyMock(return_value=msg_content)
    
    mock_channel = MagicMock()
    type(mock_channel).name = PropertyMock(return_value=channel_name)
    type(mock_message).channel = PropertyMock(return_value=mock_channel)

    if user_roles is not None:
        mock_member = MagicMock()

        type(mock_member).roles = user_roles
        
        mock_edit = MagicMock(return_value=Future())
        mock_edit.return_value.set_result(None)
        type(mock_member).edit = mock_edit
        
        type(mock_message).author = PropertyMock(return_value=mock_member)

    mock_message.delete = MagicMock(return_value=Future())
    mock_message.delete.return_value.set_result(None) 

    return mock_message 