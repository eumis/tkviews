from tkinter import END, INSERT, Text

from pyviews.presenter import Presenter


class TextPresenter(Presenter):

    @property
    def text(self) -> Text:
        return self._references['text'].instance

    def on_rendered(self):
        self.text.insert(INSERT, "Hello.....")
        self.text.insert(END, "Bye Bye.....")

        self.text.tag_add("here", "1.0", "1.4")
        self.text.tag_add("start", "1.8", "1.13")
        self.text.tag_config("here", background = "yellow", foreground = "blue")
        self.text.tag_config("start", background = "black", foreground = "green")
