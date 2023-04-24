"""Checkbutton demo view models"""

from pyviews.core.binding import BindableEntity


class SpinboxViewModel(BindableEntity):
    """Check button view model"""

    def __init__(self):
        super().__init__()
        self.int_value = None
        self.str_value = None
        self.str_values = ['one', 'two', 'three']
