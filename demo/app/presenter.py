"""Demo application presenter"""
from itertools import groupby
from tkinter.ttk import Treeview
from typing import cast

from pyviews.core import ObservableEntity
from pyviews.presenter import Presenter

from demo.model import Demo


class AppPresenter(ObservableEntity, Presenter):
    """Demo presenter"""

    def __init__(self):
        ObservableEntity.__init__(self)
        Presenter.__init__(self)
        self._demos = [
            Demo("Widgets", "Button", "button/button"),
            Demo("Widgets", "Canvas", "canvas/canvas"),
            Demo("Widgets", "Checkbutton", "checkbutton/checkbutton"),
            Demo("Widgets", "Entry", "entry/entry"),
            Demo("Widgets", "Frame", "frame/frame"),
            Demo("Widgets", "Label", "label/label"),
            Demo("Widgets", "Labelframe", "labelframe/labelframe"),

            Demo("Containers", "For", "for/for"),
            Demo("Containers", "If", "if/if"),
        ]
        self.demo_view = None
        self.demo_name = None
        self._default_demo = self._demos[0]

    @property
    def demo_tree(self) -> Treeview:
        return self._references['demo_tree'].instance

    def on_rendered(self):
        """Add demo items to tree"""
        for i, (section, demos) in enumerate(groupby(self._demos, lambda d: d.section)):
            section_item = self.demo_tree.insert("", i, section, text=section)
            for demo_i, demo in enumerate(demos):
                self.demo_tree.insert(section_item, demo_i, iid=demo.name, text=demo.name,
                                      values=[demo.view, demo.name])
                if demo == self._default_demo:
                    self.demo_view = demo.view
                    self.demo_name = demo.name
        self.demo_tree.bind('<<TreeviewSelect>>', lambda e: self._open_selected())
        self.demo_tree.see(self._default_demo.name)
        self.demo_tree.selection_add(self._default_demo.name)

    def _open_selected(self):
        selected_items = self.demo_tree.selection()
        if selected_items:
            item = self.demo_tree.item(selected_items[0])
            values = item['values']
            if values:
                self.demo_view, self.demo_name = values
