import socket

HOST = "127.0.0.1"
PORT = 65433

class ReplicatorReceiver:
    def __init__(self):
        self.receiver_to_sender_socket = socket.socket()

    def bind_socket(self):
        try:
            self.receiver_to_sender_socket.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def start_listening(self):
        print("Waiting for connections...")
        self.receiver_to_sender_socket.listen()
        # TODO - Uspostavljanje konekcije sa Sender komponentom


if __name__ == "__main__":
    replicator_receiver = ReplicatorReceiver()
    if replicator_receiver.bind_socket():
        replicator_receiver.start_listening()
