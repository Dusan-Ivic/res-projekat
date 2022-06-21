import socket
from _thread import *
import threading

HOST = "127.0.0.1"
PORT = 65430

class Logger:   
    def __init__(self):
        self.logger_socket = socket.socket()

    def initialize_socket(self):
        try:
            self.logger_socket.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))
            return False
        return True
      
    def threaded_capture(self, connection, address):
        global_lock = threading.Lock()
        while True:
            try:
                data = connection.recv(2048)
            except ConnectionResetError:
                break
            if not data:
                break
            else:
                data_decoded = data.decode("utf-8")
                print(f"Source: {address[0]}:{address[1]} {data_decoded}")
                while global_lock.locked():
                    continue

                global_lock.acquire()

                with open("logger.txt", "a+") as file:
                    file.write(data_decoded)
                    file.close()
                    
                global_lock.release()
        connection.close()

    def start_listening(self):
        print("Logger is active and waiting for connections.")
        print("---------------------------------------------")
        self.logger_socket.listen()
        while True:
            connection, address = self.logger_socket.accept()
            start_new_thread(self.threaded_capture, (connection, address))
            print(f"New connection: {address[0]}:{address[1]} \n")

if __name__ == "__main__":
    logger = Logger()
    if logger.initialize_socket():
        logger.start_listening()