import socket
from _thread import *
from datetime import datetime

HOST = "127.0.0.1"
PORT = 65432
LOG_PORT = 65430
NEW_LINE = '\n'


class ReplicatorSender:
    def __init__(self):  # pragma: no cover
        self.sender_to_writer_socket = socket.socket()
        self.sender_to_receiver_socket = socket.socket()
        self.sender_to_logger_socket = socket.socket()
    
    def initialize_socket(self):  # pragma: no cover
        try:
            self.sender_to_writer_socket.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True
    
    def connect_to_receiver(self):  # pragma: no cover
        try:
            self.sender_to_receiver_socket.connect((HOST, 65433))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def connect_to_logger(self):  # pragma: no cover
        try:
            self.sender_to_logger_socket.connect((HOST, LOG_PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def send_data_to_receiver(self, data):  # pragma: no cover
        decoded = data.decode()
        data_log = f"[SENDER] {datetime.now()} {decoded}{NEW_LINE}"
        self.sender_to_receiver_socket.send(data)
        self.sender_to_logger_socket.send(data_log.encode())

    def threaded_writer(self, connection, address):  # pragma: no cover
        while True:
            try:
                data = connection.recv(2048)
            except ConnectionResetError:
                break
            if not data:
                break
            else:
                code = data.decode("utf-8").split(",")[0]
                value = data.decode("utf-8").split(",")[1]
                print(f"[{address[0]}:{address[1]}] CODE: {code}; VALUE: {value}")
                self.send_data_to_receiver(data)
        connection.close()

    def start_listening(self):  # pragma: no cover
        print("Waiting for connections...")
        self.sender_to_writer_socket.listen()
        while True:
            connection, address = self.sender_to_writer_socket.accept()
            start_new_thread(self.threaded_writer, (connection, address))
            print(f"Writer connected from: {address[0]}:{address[1]}")

if __name__ == "__main__":  # pragma: no cover
    replicator_sender = ReplicatorSender()
    if replicator_sender.initialize_socket():
        if replicator_sender.connect_to_receiver():
            if replicator_sender.connect_to_logger():
                replicator_sender.start_listening()
