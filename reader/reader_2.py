from reader import Reader

if __name__ == "__main__":
    print("READER #2")
    reader = Reader(2, 65435)
    if reader.bind_socket():
        reader.start_receiving_data()