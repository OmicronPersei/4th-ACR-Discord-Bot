from forum_watcher.xen_foro.request_factory import RequestFactory
import unittest
from asynctest import TestCase

class TestRequestFactoryCreateThreadGetRequest(TestCase):
    def runTest(self):
        api_token = "SDfasfs"
        forum_id = "123"
        base_url = "https://myform.xyz"

        actual = RequestFactory().create_thread_get_request(api_token, forum_id, base_url)

        assert actual.get_full_url() == "https://myform.xyz/forums/123"
        assert actual.get_method() == "GET"
        assert actual.has_header("Xf-api-key")
        assert actual.get_header("Xf-api-key") == api_token
        assert actual.has_header("Content-type")
        assert actual.get_header("Content-type") == "application/json"