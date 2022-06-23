from datetime import datetime
import socket
from database.database_handler import DatabaseHandler

HOST = "127.0.0.1"
STARTING_PORT = 65434
LOG_PORT = 65430
NEW_LINE = '\n'

class Reader:
    def __init__(self, dataset, port):  # pragma: no cover
        self.dataset = dataset
        self.port = port
        self.reader_to_receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.reader_to_logger_socket = socket.socket()

    def bind_socket(self):  # pragma: no cover
        try:
            self.reader_to_receiver_socket.bind((HOST, self.port))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def connect_to_logger(self):  # pragma: no cover
        try:
           self.reader_to_logger_socket.connect((HOST, LOG_PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def calculate_deadband(self, current_value, new_value): 
        deadband = abs(new_value - current_value) / current_value * 100
        return deadband

    def process_received_data(self, id, new_code, new_value):  # pragma: no cover
        database = DatabaseHandler(self.dataset)
        if database.connect_to_database():
            database.create_table_if_not_exists()
            if database.entity_exists(id):
                if new_code == "CODE_DIGITAL":
                    database.update_entity(id, new_code, new_value)
                    data = f"{id},{new_code},{new_value}"
                    data_log = f"[READER] {datetime.now()} {data}{NEW_LINE}"
                    self.reader_to_logger_socket.send(data_log.encode())
                else:
                    current_value = database.get_entity_value(id)
                    deadband = self.calculate_deadband(current_value, new_value)
                    if deadband >= 2:
                        database.update_entity(id, new_code, new_value)
                        data = f"{id},{new_code},{new_value}"
                        data_log = f"[READER] {datetime.now()} {data}{NEW_LINE}"
                        self.reader_to_logger_socket.send(data_log.encode())
            else:
                database.insert_entity(id, new_code, new_value)
                data = f"{id},{new_code},{new_value}"
                data_log = f"[READER] {datetime.now()} {data}{NEW_LINE}"
                self.reader_to_logger_socket.send(data_log.encode())

    def start_receiving_data(self):  # pragma: no cover
        print("Waiting for connections...")
        while True:
            try:
                data, address = self.reader_to_receiver_socket.recvfrom(1024)
                print(f"Data received  from: {address[0]}:{address[1]}")
            except ConnectionResetError:
                break
            if not data:
                break
            else:
                id = data.decode().split(",")[0]
                code = data.decode().split(",")[1]
                value = data.decode().split(",")[2]
                print(f"{id},{code},{value}")
                self.process_received_data(int(id), code, int(value))

        self.reader_to_receiver_socket.close()

if __name__ == "__main__":  # pragma: no cover
    pass
