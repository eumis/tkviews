from tkinter import StringVar

class IntVar(StringVar):
    def get(self):
        return self._to_int(super().get())

    def _to_int(self, value):
        if value and value.strip():
            return int(value)
        return None
