"""Checkbutton demo view models"""
from pyviews.core import ObservableEntity


class RadioViewModel(ObservableEntity):
    """Check button view model"""

    def __init__(self):
        super().__init__()
        self.bool_value = False
        self.int_value = 10
        self.str_value = 'some value'
