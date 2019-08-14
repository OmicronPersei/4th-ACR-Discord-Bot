from unittest.mock import MagicMock, PropertyMock

def create_mock_user(display_name_val="stub_name_here", id=2343243, roles=None):
    mock_user = MagicMock()
    type(mock_user).display_name = PropertyMock(return_value=display_name_val)
    type(mock_user).id = PropertyMock(return_value=id)
    type(mock_user).roles = PropertyMock(return_value=roles)
    return mock_user

def create_mock_role(id, name):
    role = MagicMock()
    type(role).id = PropertyMock(return_value=int(id))
    type(role).name = PropertyMock(return_value=name)
    return role

class AsyncIterator:
    def __init__(self, items):
        self._items = list(items)
        self._index = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._index >= len(self._items):
            raise StopAsyncIteration
        item = self._items[self._index]
        self._index = self._index + 1
        return item