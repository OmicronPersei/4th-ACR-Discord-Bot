from unittest import TestCase
from xen_foro_forum_thread_url_factory import XenForoForumThreadURLFactory

class XenForoForumThreadURLFactoryTest(TestCase):
    def _test_returns_expected(self, base_url, forum_id, thread_id, expected_result):
        factory = XenForoForumThreadURLFactory()
        actual = factory.get_url(base_url, forum_id, thread_id)

        assert expected_result == actual

    def runTest(self):
        self._test_returns_expected("http://forum.com", "123", "456", "http://forum.com/forums/123/456")
        self._test_returns_expected("http://forum.com/", "123", "456", "http://forum.com/forums/123/456")
        self._test_returns_expected("http://forum.com/", 123, 456, "http://forum.com/forums/123/456")