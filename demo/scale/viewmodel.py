"""Checkbutton demo view models"""
from pyviews.core import ObservableEntity


class ScaleViewModel(ObservableEntity):
    """Check button view model"""

    def __init__(self):
        super().__init__()
        self.value = 0.0
