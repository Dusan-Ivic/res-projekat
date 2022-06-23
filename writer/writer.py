import socket, random
from time import sleep
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65432
LOG_PORT = 65430
NEW_LINE = '\n'

CODE_LIST = [
    "CODE_ANALOG",
    "CODE_DIGITAL",
    "CODE_CUSTOM",
    "CODE_LIMITSET",
    "CODE_SINGLENODE",
    "CODE_MULTIPLENODE",
    "CODE_CONSUMER",
    "CODE_SOURCE"]

class Writer():
    def __init__(self):  # pragma: no cover
        self.client_socket = socket.socket()
        self.client_log = socket.socket()

    def connect_to_server(self):  # pragma: no cover
        try:
            self.client_socket.connect((HOST, PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def connect_to_logger(self):  # pragma: no cover
        try:
            self.client_log.connect((HOST, LOG_PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True
    
    def get_code(self, index):
        if index < 0 or index > 7:
            raise Exception("Index out of bounds")
        return CODE_LIST[index]

    def send_data(self):  # pragma: no cover
        while True:
            value = random.randint(0, 9)
            index = random.randint(0, 7)
            code = self.get_code(index)
            str = f"{code},{value}"
            str_log = f"[WRITER] {datetime.now()} {str}{NEW_LINE}"
            self.client_socket.send(str.encode())
            self.client_log.send(str_log.encode())
            sleep(2)

if __name__ == "__main__":  # pragma: no cover
    writer = Writer()
    if writer.connect_to_server():
        if writer.connect_to_logger():
            writer.send_data()
