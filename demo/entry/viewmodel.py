"""Entry demo view models"""

from pyviews.core.binding import BindableEntity


class EntryViewModel(BindableEntity):
    """Entry view model"""

    def __init__(self):
        super().__init__()
        self.value = 'value'
