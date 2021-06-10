from tkinter import Scrollbar, Listbox

from pyviews.presenter import Presenter


class ScrollboxPresenter(Presenter):

    @property
    def scrollbar(self) -> Scrollbar:
        return self._references['scrollbar'].instance

    @property
    def listbox(self) -> Listbox:
        return self._references['listbox'].instance

    def on_rendered(self):
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)
