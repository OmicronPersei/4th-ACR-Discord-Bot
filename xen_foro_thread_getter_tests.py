from xen_foro_thread_getter import XenForoThreadGetter
from forum_thread_data_storage import ForumThreadDataStorage
import unittest
from asynctest import TestCase, MagicMock

class MockXenForoThreadGetter(XenForoThreadGetter):
    def __init__(self, mock_json_response, xen_foro_request_factory):
        super().__init__(xen_foro_request_factory)

        self.mock_json_response = mock_json_response

    def get_response(self, request):
        return self.mock_json_response

class BaseXenForoThreadGetter(TestCase):
    def setUp(self):
        self.api_token = "SDfasdf"
        self.base_url = "https://asdfdsafsda.com"
        self.forum_id = "123"
        
        self.mock_xen_foro_request_factory = MagicMock()
        self.mock_request = object()
        self.mock_xen_foro_request_factory.create_thread_get_request = MagicMock(return_value=self.mock_request)
        
        self.mock_json_response = """

        """
        
        self.mock_xen_foro_thread_request_getter = MockXenForoThreadGetter(self.mock_json_response, self.mock_xen_foro_request_factory)
        



