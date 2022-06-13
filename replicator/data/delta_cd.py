
class DeltaCD:
    def __init__(self):
        self.add = []
        self.update = []

    def ready_to_process(self):
        return len(self.add) + len(self.update) >= 10

    def clear(self):
        self.add = []
        self.update = []