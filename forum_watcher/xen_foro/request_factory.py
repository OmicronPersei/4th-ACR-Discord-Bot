import urllib.request

class RequestFactory:
    
    def create_thread_get_request(self, api_token, forum_id, base_url):
        url = "{}/forums/{}".format(base_url, forum_id)
        req = urllib.request.Request(url, headers={"xf-api-key": api_token})
        return req