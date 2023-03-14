"""Button demo view models"""

from pyviews.core.bindable import BindableEntity


class CounterViewModel(BindableEntity):
    """Counter button view model"""

    def __init__(self):
        super().__init__()
        self.count = 0

    def add_count(self):
        """Adds 1 to count"""
        self.count = self.count + 1
