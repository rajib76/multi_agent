import pickle
import sqlite3
from sqlite3 import Error

create_table_sql = f"""
CREATE TABLE IF NOT EXISTS CHKPT (
session_id TEXT PRIMARY KEY,
chkpt BLOB
);
"""


class SQLLiteClient():
    def __init__(self, db_file="/Users/joyeed/multi-agent/multi_agent/chkpt.db"):
        self.module = __name__
        self.db_file = db_file

    def connect_to_db(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e)

        return conn

    def create_chkpt_table(self, create_table_sql):
        conn = self.connect_to_db()
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

        conn.close()

    def insert_chkpt(self, record):
        self.create_chkpt_table(create_table_sql=create_table_sql)
        conn = self.connect_to_db()

        sql = '''INSERT OR REPLACE INTO CHKPT(session_id,chkpt) VALUES (?,?)'''
        cur = conn.cursor()
        cur.execute(sql, record)
        conn.commit()
        conn.close()

        return cur.lastrowid

    def select_chkpt(self, session_id):
        conn = self.connect_to_db()
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT chkpt FROM CHKPT WHERE session_id = ?",
                (session_id,),
            )
            if value := cur.fetchone():
                return pickle.loads(value[0])
        except Exception as e:
            print(e)


if __name__ == "__main__":
    client = SQLLiteClient()
    record = ("1", "raj", "{}")
    client.insert_chkpt(record=record)
    record = client.select_chkpt()
    print(record)
