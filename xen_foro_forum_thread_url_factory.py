class XenForoForumThreadURLFactory:
    def get_url(self, base_url, forum_id, thread_id):
        if base_url[-1] == "/":
            base_url = base_url[0:-1]
        return "{}/forums/{}/{}".format(base_url, str(forum_id), str(thread_id))