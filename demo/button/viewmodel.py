from pyviews.core import ObservableEntity


class CounterViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.count = 0

    def add_count(self):
        self.count = self.count + 1
