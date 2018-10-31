'''Customizing of tk parsing'''

from tkinter import Entry, Checkbutton, Radiobutton
from tkinter.ttk import Widget as TtkWidget
from pyviews import Node
from pyviews.rendering.node import get_inst_type, create_inst
from pyviews.core.xml import XmlNode
from tkviews.core.widgets import WidgetNode, EntryNode, CheckbuttonNode, RadiobuttonNode
from tkviews.core.ttk import TtkWidgetNode

def create_node(xml_node: XmlNode, **init_args):
    '''Creates node from xml node using namespace as module and tag name as class name'''
    inst_type = get_inst_type(xml_node)
    init_args['xml_node'] = xml_node
    inst = create_inst(inst_type, **init_args)
    if not isinstance(inst, Node):
        inst = _convert_to_node(inst, **init_args)
    return inst

def _convert_to_node(inst, **init_args):
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
