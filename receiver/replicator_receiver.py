from datetime import datetime
import socket, random
from data.receiver_property import ReceiverProperty
from data.collection_description import CollectionDescription
from data.delta_cd import DeltaCD

HOST = "127.0.0.1"
PORT = 65433
LOG_PORT = 65430
NEW_LINE = '\n'

class ReplicatorReceiver:
    def __init__(self):  # pragma: no cover
        self.receiver_to_sender_socket = socket.socket()
        self.receiver_to_logger_socket = socket.socket()
        self.receiver_to_reader_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.collection_descriptions = {}
        self.delta = DeltaCD()

    def bind_socket(self):  # pragma: no cover
        try:
            self.receiver_to_sender_socket.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def connect_to_logger(self):  # pragma: no cover
        try:
            self.receiver_to_logger_socket.connect((HOST, LOG_PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True

    def get_dataset(self, code):
        if code in ["CODE_ANALOG", "CODE_DIGITAL"]:
            return 1
        elif code in ["CODE_CUSTOM", "CODE_LIMITSET"]:
            return 2
        elif code in ["CODE_SINGLENODE", "CODE_MULTIPLENODE"]:
            return 3
        elif code in ["CODE_CONSUMER", "CODE_SOURCE"]:
            return 4
        else:
            raise TypeError("Code not found")

    def send_delta_to_reader(self):  # pragma: no cover
        for id in self.delta.add:
            for prop in self.delta.add[id].historical_collection.receiver_properties:
                data = f"{id},{prop.code},{prop.value}"
                print(f"\t{data}")
                self.receiver_to_reader_socket.sendto(data.encode(), (HOST, PORT + self.delta.add[id].dataset))
                log_data = f"[RECEIVER - DELTA ADD] {datetime.now()},{data}{NEW_LINE}"
                self.receiver_to_logger_socket.send(log_data.encode())

        for id in self.delta.update:
            for prop in self.delta.update[id].historical_collection.receiver_properties:
                data = f"{id},{prop.code},{prop.value}"
                print(f"\t{data}")
                self.receiver_to_reader_socket.sendto(data.encode(), (HOST, PORT + self.delta.update[id].dataset))
                log_data = f"[RECEIVER - DELTA UPDATE] {datetime.now()},{data}{NEW_LINE}"
                self.receiver_to_logger_socket.send(log_data.encode())

        self.delta.clear()

    def process_received_data(self, code, value, dataset, id):  # pragma: no cover
        receiver_property = ReceiverProperty(code, value)

        if self.delta.ready_to_process():
            print("\nSending Data from Delta to Reader...")
            self.send_delta_to_reader()
        
        if id in self.collection_descriptions:
            print(f"Adding ({code}, {value}) to Delta->Update")
            self.collection_descriptions[id].historical_collection.receiver_properties.append(receiver_property)
            collection_description = CollectionDescription(id, dataset)
            collection_description.historical_collection.receiver_properties.append(receiver_property)
            if id in self.delta.update:
                self.delta.update[id].historical_collection.receiver_properties.append(receiver_property)
            else:
                collection_description = CollectionDescription(id, dataset)
                collection_description.historical_collection.receiver_properties.append(receiver_property)
                self.delta.update[id] = collection_description
        else:
            print(f"Adding ({code}, {value}) to Delta->Add")
            collection_description = CollectionDescription(id, dataset)
            collection_description.historical_collection.receiver_properties.append(receiver_property)
            self.collection_descriptions[id] = collection_description
            if id in self.delta.add:
                self.delta.add[id].historical_collection.receiver_properties.append(receiver_property)
            else:
                collection_description = CollectionDescription(id, dataset)
                collection_description.historical_collection.receiver_properties.append(receiver_property)
                self.delta.add[id] = collection_description

    def start_listening(self):  # pragma: no cover
        print("Waiting for connections...")
        self.receiver_to_sender_socket.listen()
        connection, address = self.receiver_to_sender_socket.accept()
        print(f"Sender connected from: {address[0]}:{address[1]}\n")
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
                self.process_received_data(code, value, dataset, id)
                    
        connection.close()

if __name__ == "__main__":  # pragma: no cover
    replicator_receiver = ReplicatorReceiver()
    if replicator_receiver.bind_socket():
         if replicator_receiver.connect_to_logger():
            replicator_receiver.start_listening()
