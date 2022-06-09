from data.historical_collection import HistoricalCollection

class CollectionDescription:
    def __init__(self, id, dataset):
        self.id = id
        self.dataset = dataset
        self.historical_collection = HistoricalCollection()
