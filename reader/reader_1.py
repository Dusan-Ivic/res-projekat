from reader import Reader

if __name__ == "__main__":
    print("READER #1")
    reader = Reader(1, 65434)
    if reader.bind_socket():
        reader.start_receiving_data()
