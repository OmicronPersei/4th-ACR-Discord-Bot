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

    def get_forum_records(self, forum_name_prefix, forum_id):
        get_records_query = "select * from ForumMessageHistory where forum_name_prefix='{}' and forum_id='{}'".format(forum_name_prefix, forum_id)
        cursor = self._db.execute(get_records_query)
        records = []
        for record in cursor:
            records.append({
                "forum_name_prefix": record[0],
                "forum_id": record[1],
                "thread_id": record[2],
                "discord_message_id": record[3]
            })
        return records

    