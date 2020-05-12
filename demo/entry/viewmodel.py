from pyviews.core import ObservableEntity


class EntryViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.value = 'value'
