from reader import Reader

if __name__ == "__main__":
    print("READER #4")
    reader = Reader(4, 65437)
    if reader.bind_socket():
        reader.start_receiving_data()
