class ForumThreadDataStorage:
    def __init__(self, db, forum_threads):
        self._db = db

        self.check_forums_have_allocated_storage(forum_threads)
        
    def check_forums_have_allocated_storage(self, forum_threads):
        for thread in forum_threads:
            self._db.check_forum_has_allocated_storage(thread["forum_name_prefix"], thread["forum_id"])

    def get_forum_thread_records(self, forum_thread_query):
        return self._db.get_forum_records(forum_thread_query["forum_name_prefix"], forum_thread_query["forum_id"])
