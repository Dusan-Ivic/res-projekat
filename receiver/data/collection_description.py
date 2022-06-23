from .historical_collection import HistoricalCollection

class CollectionDescription:  # pragma: no cover
    def __init__(self, id, dataset):
        self.id = id
        self.dataset = dataset
        self.historical_collection = HistoricalCollection()
