import urllib.request

class RequestFactory:
    
    def create_thread_get_request(self, api_token, forum_id, base_url):
        url = "{}/forums/{}".format(base_url, forum_id)
        req = urllib.request.Request(url)
        req.headers["Xf-api-key"] = api_token
        req.headers["Content-type"] = "application/json"
        return req