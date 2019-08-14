from unittest.mock import MagicMock, PropertyMock

def create_mock_user(mention_val, display_name_val="stub_name_here", id=None):
    mock_user = MagicMock()
    type(mock_user).mention = PropertyMock(return_value=mention_val)
    type(mock_user).display_name = PropertyMock(return_value=display_name_val)
    if id:
        type(mock_user).id = PropertyMock(return_value=id)
    return mock_user

def MockConfigurationService(config_obj):
    service = MagicMock()
    service.get = MagicMock()
    service.get.side_effect = lambda x: config_obj[x]
    return service