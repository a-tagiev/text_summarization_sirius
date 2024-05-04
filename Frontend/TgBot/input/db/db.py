import sqlite3
import logging


class ChatDB:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_chat_table(self, group_id):
        table_name = f"chat_{group_id}".replace('-', 'minus')
        create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` (message_id INTEGER PRIMARY KEY, sender_id INTEGER, message_text TEXT)"
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"SQLite error in create_chat_table: {e}")

    def insert_message(self, group_id, message_id, sender_id, message_text):
        table_name = f"chat_{group_id}".replace('-', 'minus')
        self.create_chat_table(group_id)
        insert_query = f"INSERT INTO `{table_name}` (message_id, sender_id, message_text) VALUES (?, ?, ?)"
        try:
            self.cursor.execute(insert_query, (message_id, sender_id, message_text))
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"SQLite error in insert_message: {e}")

    def get_last_messages(self, group_id, start_message_id, end_message_id):
        table_name = f"chat_{group_id}".replace('-', 'minus')
        query = f"SELECT message_text FROM `{table_name}` WHERE message_id BETWEEN ? AND ? ORDER BY message_id ASC"
        try:
            self.cursor.execute(query, (start_message_id, end_message_id))
            messages = [row[0] for row in self.cursor.fetchall()]
            filtered_messages = [message for message in messages if '@sirius_summary_bot' not in message]
            return filtered_messages

        except sqlite3.Error as e:
            logging.error(f"SQLite error in get_messages_between_ids: {e}")
            return []

    def close_connection(self):
        self.connection.close()


chat_db = ChatDB("db/chat_database.db")
