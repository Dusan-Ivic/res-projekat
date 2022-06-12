import socket

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
                print(data.decode())
                # TODO - Procesiranje primljenih podataka (na bazu podataka)

        self.reader_to_receiver_socket.close()

if __name__ == "__main__":
    pass
