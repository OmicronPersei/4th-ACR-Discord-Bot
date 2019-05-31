from xen_foro_request_factory import XenForoRequestFactory
import unittest
import asynctest

class TestXenForoRequestFactoryCreateThreadGetRequest(asynctest.TestCase):
    def runTest(self):
        api_token = "SDfasfs"
        forum_id = "123"
        base_url = "https://myform.xyz"

        actual = XenForoRequestFactory().create_thread_get_request(api_token, forum_id, base_url)

        assert actual.get_full_url() == "{}/threads/{}".format(base_url, forum_id)
        assert actual.get_method() == "GET"
        assert actual.has_header("Xf-api-key")
        assert actual.get_header("Xf-api-key") == api_token


# asynctest.main()
