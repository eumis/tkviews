from itertools import groupby
from tkinter.ttk import Treeview
from typing import cast

from pyviews.core import ObservableEntity

from demo.model import Demo


class AppPresenter(ObservableEntity):
    def __init__(self):
        super().__init__()
        self._demo_tree: Treeview = cast(Treeview, None)
        self._demos = [
            Demo("Widgets", "Button", "button/button"),
            Demo("Widgets", "Canvas", "canvas/canvas"),
            Demo("Widgets", "Checkbutton", "checkbutton/checkbutton"),
            Demo("Widgets", "Entry", "entry/entry"),
            Demo("Widgets", "Frame", "frame/frame"),
            Demo("Widgets", "Label", "label/label")
        ]
        self.demo_view = None
        self._default_demo = self._demos[-1]

    def set_demo_tree(self, demo_tree: Treeview):
        self._demo_tree = demo_tree
        for i, (section, demos) in enumerate(groupby(self._demos, lambda d: d.section)):
            section_item = self._demo_tree.insert("", i, section, text=section)
            for demo_i, demo in enumerate(demos):
                self._demo_tree.insert(section_item, demo_i, text=demo.name, values=[demo.view])
                if demo == self._default_demo:
                    self.demo_view = demo.view
        demo_tree.bind('<<TreeviewSelect>>', lambda e: self._open_selected())

    def _open_selected(self):
        selected_items = self._demo_tree.selection()
        if selected_items:
            item = self._demo_tree.item(selected_items[0])
            values = item['values']
            if values:
                self.demo_view = values[0]
