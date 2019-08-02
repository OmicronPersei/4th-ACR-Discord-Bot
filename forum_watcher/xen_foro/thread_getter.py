import urllib.request
import json

class ThreadGetter:
    def __init__(self, request_factory):
        self.request_factory = request_factory

    def get_threads(self, threads_query):
        request = self.request_factory.create_thread_get_request(threads_query["api_token"], threads_query["forum_id"], threads_query["base_url"])
        response = self._get_response(request)
        return json.loads(response)

    def _get_response(self, request):
        return urllib.request.urlopen(request)