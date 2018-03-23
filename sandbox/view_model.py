from pyviews.core.observable import ObservableEntity

class AppViewModel(ObservableEntity):
    def __init__(self, default_view=None):
        super().__init__()
        self.view = default_view

class BindingViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.entry = 'value'
        self.check_b = False
        self.check_int = 10
        self.check_str = 'some value'
        self.radio = -1
