"""Node creation"""

from tkinter import Entry, Checkbutton, Radiobutton
from tkinter.ttk import Widget as TtkWidget
from pyviews.core import Node, XmlNode
from pyviews.rendering import get_inst_type, create_inst
from tkviews.node import WidgetNode, TtkWidgetNode
from tkviews.node import EntryNode, CheckbuttonNode, RadiobuttonNode


def create_widget_node(xml_node: XmlNode, **init_args) -> WidgetNode:
    """Creates node from xml node using namespace as module and tag name as class name"""
    inst_type = get_inst_type(xml_node)
    init_args['xml_node'] = xml_node
    inst = create_inst(inst_type, **init_args)
    if not isinstance(inst, Node):
        inst = _convert_to_node(inst, **init_args)
    return inst


def _convert_to_node(inst, **init_args) -> WidgetNode:
    init_args['widget'] = inst
    node_class = WidgetNode
    if isinstance(inst, Entry):
        node_class = EntryNode
    elif isinstance(inst, Checkbutton):
        node_class = CheckbuttonNode
    elif isinstance(inst, Radiobutton):
        node_class = RadiobuttonNode
    elif isinstance(inst, TtkWidget):
        node_class = TtkWidgetNode
    return create_inst(node_class, **init_args)
