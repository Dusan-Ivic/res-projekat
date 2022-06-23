from reader import Reader

if __name__ == "__main__":  # pragma: no cover
    print("READER #1")
    reader = Reader(1, 65434)
    if reader.bind_socket():
        if reader.connect_to_logger():
            reader.start_receiving_data()
