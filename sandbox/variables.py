from tkinter import StringVar


class IntVar(StringVar):

    def get(self):
        return self._to_int(super().get())

    @staticmethod
    def _to_int(value):
        if value and value.strip():
            return int(value)
        return None
