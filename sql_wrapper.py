import sqlite3

class SQLWrapper:
    def __init__(self, config):
        self._config = config

        self._connect()

    def _connect(self):
        db_filename = self._config["db_filename"]
        self._db = self._get_db_connection(db_filename)
    
    def _get_db_connection(self, db_filename):
        return sqlite3.connect(db_filename)
    
    def check_forum_has_allocated_storage(self):
        get_a_record_query = "select 1 from ForumMessageHistory"
        try:
            self._db.execute(get_a_record_query)
        except sqlite3.OperationalError:
            new_table_query = "create table ForumMessageHistory (forum_name nvarchar, forum_id nvarchar, thread_id nvarchar)"
            self._db.execute(new_table_query)
            self._db.commit()

    def get_forum_thread_records(self, forum_name, forum_id):
        get_records_query = "select * from ForumMessageHistory where forum_name='{}' and forum_id='{}'".format(forum_name, forum_id)
        cursor = self._db.execute(get_records_query)
        records = []
        for record in cursor:
            records.append({
                "forum_name": record[0],
                "forum_id": record[1],
                "thread_id": record[2]})
        return records

    def insert_forum_thread_record(self, forum_record):
        sql_insert = """insert into ForumMessageHistory (forum_name, forum_id, thread_id)
        values ('{}', '{}', '{}')""".format(
            forum_record["forum_name"],
            forum_record["forum_id"],
            forum_record["thread_id"]
        )
        self._db.execute(sql_insert)
        self._db.commit()

    