import urllib.request
import json

class ThreadGetter:
    def __init__(self, request_factory):
        self.request_factory = request_factory

    def get_threads(self, base_url, api_token, forum_id):
        request = self.request_factory.create_thread_get_request(api_token, forum_id, base_url)
        response = self._get_response(request)
        return json.loads(response)

    def _get_response(self, request):
        return urllib.request.urlopen(request)