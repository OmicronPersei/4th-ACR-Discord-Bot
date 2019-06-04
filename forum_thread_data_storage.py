class ForumThreadDataStorage:
    def __init__(self, sql_wrapper):
        self._sql_wrapper = sql_wrapper
        
    def check_forums_have_allocated_storage(self):
        self._sql_wrapper.check_forum_has_allocated_storage()

    def get_forum_thread_records(self, forum_thread_query):
        return self._sql_wrapper.get_forum_records(forum_thread_query["forum_name"], forum_thread_query["forum_id"])

    def store_new_forum_thread_record(self, new_forum_record):
        self._sql_wrapper.insert_forum_record(new_forum_record)
