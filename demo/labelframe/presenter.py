from tkinter import LabelFrame, Button
from tkinter.colorchooser import askcolor

from pyviews.presenter import Presenter


class LabelFramePresenter(Presenter):
    @property
    def label_frame(self) -> LabelFrame:
        return self._references['label_frame'].instance

    def on_rendered(self):
        def select_color():
            color = askcolor()[1]
            self.label_frame.config(background=color)

        button = Button(self.label_frame, text='Select color', command=select_color)
        button.pack()
