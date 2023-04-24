from tkinter import StringVar
from typing import List

from pyviews.core.binding import BindableEntity


class Counter(BindableEntity):

    def __init__(self):
        super().__init__()
        self._count = None
        self._range = None
        self._add_key('count')
        self._add_key('range')
        self.count = 0
        self.index = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        old_value = self._count
        self._count = value
        if value is not None:
            self._notify('count', value, old_value)
            self._range = range(value)
            self._notify('range', self._range, None)

    @property
    def range(self) -> List[int]:
        return self._range

    def up_count(self):
        self.count += 1

    def down_count(self):
        self.count -= 1

    def up_item(self):
        try:
            self._range[self.index] = self.range[self.index] + 1
            self._notify('range', self._range, None)
        except IndexError:
            pass


class CounterVar(StringVar):

    def get(self):
        return self._to_int(super().get())

    @staticmethod
    def _to_int(value):
        if value and value.strip():
            return int(value)
        return None
