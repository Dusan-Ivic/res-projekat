import socket, random
from data.receiver_property import ReceiverProperty
from data.collection_description import CollectionDescription

HOST = "127.0.0.1"
PORT = 65433

class ReplicatorReceiver:
    def __init__(self):
        self.receiver_to_sender_socket = socket.socket()
        self.collection_descriptions = {}

    def bind_socket(self):
        try:
            self.receiver_to_sender_socket.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def get_dataset(self, code):
        if code in ["CODE_ANALOG", "CODE_DIGITAL"]:
            return 1
        if code in ["CODE_CUSTOM", "CODE_LIMITSET"]:
            return 2
        if code in ["CODE_SINGLENODE", "CODE_MULTIPLENODE"]:
            return 3
        if code in ["CODE_CONSUMER", "CODE_SOURCE"]:
            return 4

    def start_listening(self):
        print("Waiting for connections...")
        self.receiver_to_sender_socket.listen()
        connection, address = self.receiver_to_sender_socket.accept()
        with connection:
            print(f"Sender connected from: {address[0]}:{address[0]}")
            while True:
                try:
                    data = connection.recv(1024)
                except ConnectionResetError:
                    break

                if not data:
                    break
                else:
                    code = data.decode().split(",")[0]
                    value = data.decode().split(",")[1]
                    dataset = self.get_dataset(code)
                    id = random.randint(0, 100)
                    receiver_property = ReceiverProperty(code, value)

                    if id in self.collection_descriptions:
                        self.collection_descriptions[id].historical_collection.receiver_properties.append(receiver_property)
                    else:
                        collection_description = CollectionDescription(id, dataset)
                        collection_description.historical_collection.receiver_properties.append(receiver_property)
                        self.collection_descriptions[id] = collection_description

                    # TODO - Uspostavljanje komunikacije sa Reader komponentom

            connection.close()


if __name__ == "__main__":
    replicator_receiver = ReplicatorReceiver()
    if replicator_receiver.bind_socket():
        replicator_receiver.start_listening()
