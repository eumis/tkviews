"""
Nodes used as abstract containers, that used to incapsulate some logic.
Containers don't represent any widget.
"""

from tkinter import Widget
from pyviews.core import XmlNode, InheritedDict, Node
from tkviews.core import TkNode


class Container(Node, TkNode):
    """Used to combine some xml elements"""

    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self._master = master
        self._node_styles = node_styles

    @property
    def master(self):
        """Master widget"""
        return self._master

    @property
    def node_styles(self):
        return self._node_styles


class View(Container):
    """Loads xml from another file"""

    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(master, xml_node, node_globals=node_globals, node_styles=node_styles)
        self._name = None
        self.name_changed = lambda view, name, previous_name: None

    @property
    def name(self):
        """Returns view name"""
        return self._name

    @name.setter
    def name(self, value):
        old_name = self._name
        self._name = value
        self.name_changed(self, value, old_name)

    def set_content(self, content: Node):
        """Destroys current """
        self._children = [content]


class For(Container):
    """Renders children for every item in items collection"""

    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(master, xml_node, node_globals=node_globals, node_styles=node_styles)
        self._items = []
        self.items_changed = lambda node, items, old_items: None

    @property
    def items(self):
        """Returns items"""
        return self._items

    @items.setter
    def items(self, value):
        old_items = self._items
        self._items = value
        self.items_changed(self, value, old_items)


class If(Container):
    """Renders children if condition is True"""

    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(master, xml_node, node_globals=node_globals, node_styles=node_styles)
        self._condition = False
        self.condition_changed = lambda node, cond, old_cond: None

    @property
    def condition(self):
        """Returns condition"""
        return self._condition

    @condition.setter
    def condition(self, value):
        old_condition = self._condition
        self._condition = value
        self.condition_changed(self, value, old_condition)
