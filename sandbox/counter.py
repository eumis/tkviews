from pyviews.core.observable import ObservableEntity

class Counter(ObservableEntity):
    def __init__(self):
        super().__init__()
        self._count = None
        self._range = None
        self._callbacks['range'] = []
        self._callbacks['count'] = []
        self.count = 0
        self.index = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value
        if value is not None:
            old_val = self._range
            self._range = range(value)
            self._notify('range', range(value), old_val)

    @property
    def range(self):
        return self._range

    def up_count(self):
        self.count += 1

    def up_item(self):
        try:
            self._range[self.index] = self.range[self.index] + 1
            self._notify('range', self._range, None)
        except IndexError:
            pass
