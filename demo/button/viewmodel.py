"""Button demo view models"""
from pyviews.core import ObservableEntity


class CounterViewModel(ObservableEntity):
    """Counter button view model"""

    def __init__(self):
        super().__init__()
        self.count = 0

    def add_count(self):
        """Adds 1 to count"""
        self.count = self.count + 1
