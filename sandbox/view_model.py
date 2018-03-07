from pyviews.core.observable import ObservableEntity

class AppViewModel(ObservableEntity):
    def __init__(self, default_view=None):
        super().__init__()
        self.view = default_view
