from pyviews.core import ObservableEntity


class CheckViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.check_b = False
        self.check_int = 10
        self.check_str = 'some value'
