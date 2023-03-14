"""Checkbutton demo view models"""

from pyviews.core.bindable import BindableEntity


class CheckViewModel(BindableEntity):
    """Check button view model"""

    def __init__(self):
        super().__init__()
        self.check_b = False
        self.check_int = 10
        self.check_str = 'some value'
