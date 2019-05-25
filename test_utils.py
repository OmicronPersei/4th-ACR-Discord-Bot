from unittest.mock import MagicMock, PropertyMock

def create_mock_user(mention_val):
    mock_user = MagicMock()
    type(mock_user).mention = PropertyMock(return_value=mention_val)
    return mock_user