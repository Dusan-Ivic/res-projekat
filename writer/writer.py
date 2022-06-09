import socket, random
from time import sleep

HOST = "127.0.0.1"
PORT = 65432

CODE_LIST = [
    "CODE_ANALOG",
    "CODE_DIGITAL",
    "CODE_CUSTOM",
    "CODE_LIMITSET",
    "CODE_SINGLENODE",
    "CODE_MULTIPLENODE",
    "CODE_CONSUMER",
    "CODE_SOURCE"]


class Writer:
    def __init__(self):
        self.client_socket = socket.socket()

    def connect_to_server(self):
        try:
            self.client_socket.connect((HOST, PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True
    
    def get_code(self, index):
        return CODE_LIST[index]
  
    def send_data(self):
        while True:
            value = random.randint(0, 9)
            index = random.randint(0, 7)
            code = self.get_code(index)
            str = f"{code},{value}"
            self.client_socket.send(str.encode())
            sleep(2)

if __name__ == "__main__":
    writer = Writer()
    if writer.connect_to_server():
        writer.send_data()
