from typing import NamedTuple

from pyviews.core import ObservableEntity


class RadioValue(NamedTuple):
    value: int
    label: str


class ValuesViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.values = ['None', 'One', 'Two']
        self.selected = 0
