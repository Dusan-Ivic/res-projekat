import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self, dataset):
        self.dataset = dataset

    def connect_to_database(self):
        try:
            self.connection = sqlite3.connect(f"db_set{self.dataset}.db")
        except:
            return False
        return True

    def create_table_if_not_exists(self):
        try:
            self.connection.execute("""
                CREATE TABLE data
                (
                    id INT PRIMARY KEY NOT NULL,
                    code TEXT NOT NULL,
                    value INT NOT NULL,
                    timestamp TEXT NOT NULL
                )
                """)
        except:
            pass

    def get_entity(self, id):
        results = self.connection.execute(f"""
            SELECT code, value
            FROM data
            WHERE id = {id}
            """)
        return results.fetchall()[0]

    def get_all_entities(self):
        results = self.connection.execute(f"""
            SELECT id, code, value, timestamp
            FROM data
            """)
        return results.fetchall()

    def entity_exists(self, id):
        results = self.connection.execute(f"""
            SELECT id, code, value, timestamp
            FROM data
            WHERE id = {id}
            """)
        if len(results.fetchall()) > 0:
            return True
        return False

    def insert_entity(self, id, code, value):
        print("[DATABASE] INSERT ENTITY")
        timestamp = datetime.now()
        self.connection.execute(f"""
            INSERT INTO data (id, code, value, timestamp)
            VALUES ({id}, '{code}', {value}, '{timestamp}')
            """)
        self.connection.commit()

    def update_entity(self, id, code, value):
        print("[DATABASE] UPDATE ENTITY")
        timestamp = datetime.now()
        # entity = self.get_entity(id)
        # ecode, evalue = entity
        # TODO - Provera deadband-a
        self.connection.execute(f"""
            UPDATE data
            SET code = "{code}", value = {value}, timestamp = "{timestamp}"
            WHERE id = {id}
            """)
        self.connection.commit()
