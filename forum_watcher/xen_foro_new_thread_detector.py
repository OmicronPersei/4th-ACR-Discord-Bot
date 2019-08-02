class XenForoNewThreadDetector:
    def __init__(self, thread_getter, thread_data_storage, forum_config, forum_api_token):
        self._thread_getter = thread_getter
        self._thread_data_storage = thread_data_storage
        self._forum_config = forum_config
        self._forum_api_token = forum_api_token

        self._thread_data_storage.check_forums_have_allocated_storage()

    def get_threads_needing_messages(self):
        forums = self._forum_config["forums"]
        forum_base_url = self._forum_config["base_url"]
        forum_threads_needing_messages = []

        for forum in forums:
            forum_name = self._forum_config["forum_name"]
            forum_id = forum["forum_id"]
            api_token = self._forum_api_token
            data_storage_query = {
                "forum_name": forum_name,
                "forum_id": forum_id
            }

            threads_recorded = self._map_by_thread_id(self._thread_data_storage.get_forum_thread_records(data_storage_query))
            threads_on_forum = self._map_by_thread_id(self._thread_getter.get_threads(forum_base_url, api_token, forum_id))

            for thread_id,thread_forum_item in threads_on_forum.items():
                if thread_id not in threads_recorded:
                    forum_threads_needing_messages.append(thread_forum_item)

        return forum_threads_needing_messages

    def _map_by_thread_id(self, items):
        dict_by_thread_id = dict()
        for item in items:
            dict_by_thread_id[item["thread_id"]] = item
        return dict_by_thread_id

