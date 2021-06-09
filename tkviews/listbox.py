from tkinter import Listbox
from typing import Callable

from pyviews.core import Node, XmlNode, InheritedDict
from pyviews.pipes import apply_attributes
from pyviews.rendering import RenderingPipeline, RenderingError

from tkviews.core import TkRenderingContext


class ListboxItem(Node):
    def __init__(self, xml_node: XmlNode,
                 node_globals: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self.on_updated: Callable[[ListboxItem], None] = None
        self._index = None
        self._value: str = ''

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        self._index = value
        if self.on_updated is not None:
            self.on_updated(self)

    @property
    def value(self) -> str:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value
        if self.on_updated is not None:
            self.on_updated(self)


def get_listboxitem_pipeline() -> RenderingPipeline:
    """Returns setup for canvas"""
    return RenderingPipeline(pipes=[
        apply_attributes,
        insert_item,
        setup_on_updated,
        setup_on_destroy
    ])


def insert_item(node: ListboxItem, context: TkRenderingContext):
    listbox: Listbox = context.master
    if not isinstance(listbox, Listbox):
        raise RenderingError(f'{ListboxItem.__name__} parent should be Listbox')
    node.index = node.index if node.index else listbox.size()
    listbox.insert(node.index, node.value)


def setup_on_updated(node: ListboxItem, context: TkRenderingContext):
    listbox: Listbox = context.master
    node.on_updated = lambda n: _update_item(listbox, n)


def _update_item(listbox: Listbox, item: ListboxItem):
    listbox.delete(item.index)
    listbox.insert(item.index, item.value)


def setup_on_destroy(node: ListboxItem, context: TkRenderingContext):
    listbox: Listbox = context.master
    node.on_destroy = lambda n: _delete_item(listbox, n)


def _delete_item(listbox: Listbox, item: ListboxItem):
    listbox.delete(item.index)