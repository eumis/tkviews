"""Checkbutton demo view models"""

from pyviews.core.binding import BindableEntity


class ScaleViewModel(BindableEntity):
    """Check button view model"""

    def __init__(self):
        super().__init__()
        self.value = 0.0
