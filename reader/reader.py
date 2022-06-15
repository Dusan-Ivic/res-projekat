import socket
from database_handler import DatabaseHandler

HOST = "127.0.0.1"
STARTING_PORT = 65434

class Reader:
    def __init__(self, dataset, port):
        self.dataset = dataset
        self.port = port
        self.reader_to_receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_socket(self):
        try:
            self.reader_to_receiver_socket.bind((HOST, self.port))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def calculate_deadband(self, current_value, new_value):
        deadband = abs(new_value - current_value) / current_value * 100
        return deadband

    def process_received_data(self, id, new_code, new_value):
        database = DatabaseHandler(self.dataset)
        if database.connect_to_database():
            database.create_table_if_not_exists()
            if database.entity_exists(id):
                if new_code == "CODE_DIGITAL":
                    database.update_entity(id, new_code, new_value)
                else:
                    current_value = database.get_entity_value(id)
                    deadband = self.calculate_deadband(current_value, new_value)
                    if deadband >= 2:
                        database.update_entity(id, new_code, new_value)
            else:
                database.insert_entity(id, new_code, new_value)

    def start_receiving_data(self):
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

if __name__ == "__main__":
    pass
