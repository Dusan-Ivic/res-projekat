from reader import Reader

if __name__ == "__main__":
    print("READER #3")
    reader = Reader(3, 65436)
    if reader.bind_socket():
        reader.start_receiving_data()
