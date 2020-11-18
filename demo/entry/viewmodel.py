"""Entry demo view models"""
from pyviews.core import ObservableEntity


class EntryViewModel(ObservableEntity):
    """Entry view model"""

    def __init__(self):
        super().__init__()
        self.value = 'value'
