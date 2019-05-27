from unittest import TestCase
from xen_foro_forum_thread_url_factory import XenForoForumThreadURLFactory

class XenForoForumThreadURLFactoryTest(TestCase):
    def _test_returns_expected(self, base_url, thread_title, expected_result):
        factory = XenForoForumThreadURLFactory()
        actual = factory.get_url(base_url, thread_title)

        assert expected_result == actual

    def runTest(self):
        self._test_returns_expected("http://forum.com", "my_thread", "http://forum.com/threads/my_thread")
        self._test_returns_expected("http://forum.com/", "my_thread", "http://forum.com/threads/my_thread")