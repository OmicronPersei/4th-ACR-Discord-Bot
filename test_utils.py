from unittest.mock import MagicMock, PropertyMock

def create_mock_user(mention_val, display_name_val="stub_name_here"):
    mock_user = MagicMock()
    type(mock_user).mention = PropertyMock(return_value=mention_val)
    type(mock_user).display_name = PropertyMock(return_value=display_name_val)
    return mock_user