import socket

HOST = "127.0.0.1"
STARTING_PORT = 65444

class Reader:
    def __init__(self, dataset, port):
        self.dataset = dataset
        self.port = port
        self.reader_to_receiver_socket = socket.socket()

    def bind_socket(self):
        try:
            self.receiver_to_sender_socket.bind((HOST, self.port))
        except socket.error as e:
            print(str(e))
            return False
        return True

if __name__ == "__main__":
    for i in range(4):
        reader = Reader(i + 1, STARTING_PORT + i)
        if reader.bind_socket():
            pass
