from xen_foro_thread_getter import XenForoThreadGetter
from forum_thread_data_storage import ForumThreadDataStorage
import unittest
from asynctest import TestCase, MagicMock

class MockXenForoThreadGetter(XenForoThreadGetter):
    def __init__(self, mock_json_response, xen_foro_request_factory):
        super().__init__(xen_foro_request_factory)

        self.mock_json_response = mock_json_response

    def _get_response(self, request):
        return self.mock_json_response

class TestXenForoThreadGetter(TestCase):
    def setUp(self):
        self.api_token = "SDfasdf"
        self.base_url = "https://asdfdsafsda.com"
        self.forum_id = "123"
        
        self.mock_xen_foro_request_factory = MagicMock()
        self.mock_request = object()
        self.mock_xen_foro_request_factory.create_thread_get_request = MagicMock(return_value=self.mock_request)
        
        self.mock_json_response = """
        {
            \"my prop\": \"my val\"
        }
        """
        
        self.mock_xen_foro_thread_request_getter = MockXenForoThreadGetter(self.mock_json_response, self.mock_xen_foro_request_factory)

    def runTest(self):
        actual = self.mock_xen_foro_thread_request_getter.get_threads(self.base_url, self.api_token, self.forum_id)

        self.mock_xen_foro_request_factory.create_thread_get_request.assert_called_with(self.api_token, self.forum_id, self.base_url)
        assert actual["my prop"] == "my val"
        



