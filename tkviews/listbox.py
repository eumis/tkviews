from tkinter import Listbox
from typing import Callable, Optional

from pyviews.core.rendering import Node, NodeGlobals, RenderingError
from pyviews.core.xml import XmlNode
from pyviews.pipes import apply_attributes
from pyviews.rendering.pipeline import RenderingPipeline

from tkviews.core import TkRenderingContext


class ListboxItem(Node):

    def __init__(self, xml_node: XmlNode, node_globals: Optional[NodeGlobals] = None):
        super().__init__(xml_node, node_globals = node_globals)
        self.on_updated: Optional[Callable[[ListboxItem], None]] = None
        self._index: Optional[int] = None
        self._value: str = ''

    @property
    def index(self) -> Optional[int]:
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


def get_listboxitem_pipeline() -> RenderingPipeline[ListboxItem, TkRenderingContext]:
    """Returns setup for canvas"""
    return RenderingPipeline[ListboxItem, TkRenderingContext](pipes=[
        apply_attributes,
        insert_item,
        setup_on_updated,
        setup_on_destroy
    ]) # yapf: disable


def insert_item(node: ListboxItem, context: TkRenderingContext):
    if not isinstance(context.master, Listbox):
        raise RenderingError(f'{ListboxItem.__name__} parent should be Listbox')
    listbox: Listbox = context.master
    node.index = node.index if node.index else listbox.size()
    listbox.insert(node.index, node.value)


def setup_on_updated(node: ListboxItem, context: TkRenderingContext):
    if not isinstance(context.master, Listbox):
        raise RenderingError(f'{ListboxItem.__name__} parent should be Listbox')
    listbox: Listbox = context.master
    node.on_updated = lambda n: _update_item(listbox, n)


def _update_item(listbox: Listbox, item: ListboxItem):
    listbox.delete(item.index)
    listbox.insert(item.index, item.value)


def setup_on_destroy(node: ListboxItem, context: TkRenderingContext):
    if not isinstance(context.master, Listbox):
        raise RenderingError(f'{ListboxItem.__name__} parent should be Listbox')
    listbox: Listbox = context.master
    node.on_destroy = lambda n: _delete_item(listbox, n)


def _delete_item(listbox: Listbox, item: ListboxItem):
    listbox.delete(item.index)
