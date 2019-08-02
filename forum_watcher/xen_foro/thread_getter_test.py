from forum_watcher.xen_foro.thread_getter import ThreadGetter
from forum_watcher.forum_thread_data_storage import ForumThreadDataStorage
from asynctest import TestCase, MagicMock

class MockThreadGetter(ThreadGetter):
    def __init__(self, mock_json_response, request_factory):
        super().__init__(request_factory)

        self.mock_json_response = mock_json_response

    def _get_response(self, request):
        return self.mock_json_response

class TestThreadGetter(TestCase):
    def setUp(self):
        self.api_token = "SDfasdf"
        self.base_url = "https://asdfdsafsda.com"
        self.forum_id = "123"
        
        self.mock_request_factory = MagicMock()
        self.mock_request = object()
        self.mock_request_factory.create_thread_get_request = MagicMock(return_value=self.mock_request)
        
        self.mock_json_response = """
        {
            \"my prop\": \"my val\"
        }
        """
        
        self.mock_thread_request_getter = MockThreadGetter(self.mock_json_response, self.mock_request_factory)

    def runTest(self):
        thread_query = {
            "base_url": self.base_url,
            "api_token": self.api_token,
            "forum_id": self.forum_id
        }
        actual = self.mock_thread_request_getter.get_threads(thread_query)

        self.mock_request_factory.create_thread_get_request.assert_called_with(self.api_token, self.forum_id, self.base_url)
        assert actual["my prop"] == "my val"
        



