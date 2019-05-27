import sqlite3

class SQLWrapper:
    def __init__(self, config):
        self._config = config

        self.connect()

    def connect(self):
        db_filename = self._config["db_filename"]
        self._db = self.get_db_connection(db_filename)
    
    def get_db_connection(self, db_filename):
        return sqlite3.connect(db_filename)
    
    def check_forum_has_allocated_storage(self, forum_name_prefix, forum_id):
        get_a_record_query = "select top 1 * from ForumMessageHistory"
        try:
            self._db.execute(get_a_record_query)
        except sqlite3.OperationalError:
            new_table_query = "create table ForumMessageHistory (forum_name_prefix nvarchar, forum_id nvarchar, thread_id nvarchar, discord_message_id nvarchar)"
            self._db.execute(new_table_query)
            self._db.commit()
    