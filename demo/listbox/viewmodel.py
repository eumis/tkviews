from typing import Tuple

from pyviews.core import ObservableEntity


class ListboxItemsViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.items = ['one', 'two', 'three']

    def delete(self, indexes: Tuple[int]):
        indexes = set(indexes)
        new_items = [v for i, v in enumerate(self.items) if i not in indexes]
        self.items = new_items
