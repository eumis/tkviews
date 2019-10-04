"""Node creation"""

from tkinter import Entry, Checkbutton, Radiobutton
from tkinter.ttk import Widget as TtkWidget
from typing import Type

from pyviews.core import Node, XmlNode
from pyviews.rendering import get_inst_type, create_inst
from tkviews.node import WidgetNode, TtkWidgetNode
from tkviews.node import EntryNode, CheckbuttonNode, RadiobuttonNode
from tkviews.rendering.common import TkRenderingContext


def create_widget_node(xml_node: XmlNode, context: TkRenderingContext) -> WidgetNode:
    """Creates node from xml node using namespace as module and tag name as class name"""
    inst_type = get_inst_type(xml_node)
    context['xml_node'] = xml_node
    inst = create_inst(inst_type, context)
    if not isinstance(inst, Node):
        inst = _convert_to_node(inst, context)
    return inst


def _convert_to_node(inst: Type, context: TkRenderingContext) -> WidgetNode:
    context['widget'] = inst
    node_class = WidgetNode
    if isinstance(inst, Entry):
        node_class = EntryNode
    elif isinstance(inst, Checkbutton):
        node_class = CheckbuttonNode
    elif isinstance(inst, Radiobutton):
        node_class = RadiobuttonNode
    elif isinstance(inst, TtkWidget):
        node_class = TtkWidgetNode
    return create_inst(node_class, context)
