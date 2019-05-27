class ForumThreadDataStorage:
    def __init__(self, db, forum_threads):
        self._db = db

        self.check_forums_have_allocated_storage(forum_threads)
        
    def check_forums_have_allocated_storage(self, forum_threads):
        for thread in forum_threads:
            self._db.check_forum_has_allocated_storage(thread["forum_name_prefix"], thread["thread_id"])
