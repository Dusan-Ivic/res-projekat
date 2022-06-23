from reader import Reader

if __name__ == "__main__":  # pragma: no cover
    print("READER #2")
    reader = Reader(2, 65435)
    if reader.bind_socket():
        if reader.connect_to_logger():
            reader.start_receiving_data()
