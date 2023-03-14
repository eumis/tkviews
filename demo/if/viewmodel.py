from typing import NamedTuple

from pyviews.core.bindable import BindableEntity


class RadioValue(NamedTuple):
    value: int
    label: str


class ValuesViewModel(BindableEntity):

    def __init__(self):
        super().__init__()
        self.values = ['None', 'One', 'Two']
        self.selected = 0
