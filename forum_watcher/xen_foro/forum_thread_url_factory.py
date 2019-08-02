class ForumThreadURLFactory:
    def get_url(self, base_url, thread_name):
        if base_url[-1] == "/":
            base_url = base_url[0:-1]
        return "{}/threads/{}".format(base_url, thread_name)