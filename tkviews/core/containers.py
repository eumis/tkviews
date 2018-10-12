'''
Nodes used as abstract containers, that used to incapsulate some logic.
Containers don't represent any widget.
'''

from tkinter import Widget
from pyviews.core.xml import XmlNode
from pyviews.core.observable import InheritedDict, observable_property
from pyviews.core.node import Node
from tkviews.core import TkNode

class Container(Node, TkNode):
    '''Used to combine some xml elements'''
    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self._master = master
        self._node_styles = node_styles

    @property
    def master(self):
        '''Master widget'''
        return self._master

    @property
    def node_styles(self):
        return self._node_styles

class View(Container):
    '''Loads xml from anothre file'''
    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(master, xml_node, node_globals=node_globals, node_styles=node_styles)

    (name, name_observable) = observable_property('_name')

    def set_content(self, content: Node):
        '''Destroys current '''
        self._children = [content]

class For(Container):
    '''Renders children for every item in items collection'''
    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(master, xml_node, node_globals=node_globals, node_styles=node_styles)
        self.items = []

    (items, items_observable) = observable_property('_items')

class If(Container):
    '''Renders children if condition is True'''
    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(master, xml_node, node_globals=node_globals, node_styles=node_styles)
        self.condition = False

    (condition, condition_observable) = observable_property('_condition')
