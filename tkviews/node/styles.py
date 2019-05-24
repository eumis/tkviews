"""Nodes for storing config options for widgets"""

from typing import Any
from pyviews.core import CoreError, XmlNode, Node, InheritedDict, Modifier


class StyleError(CoreError):
    """Error for style"""


class StyleItem:
    """Wrapper under option"""

    def __init__(self, modifier: Modifier, name: str, value: Any):
        self._modifier = modifier
        self._name = name
        self._value = value

    @property
    def setter(self):
        """Returns setter"""
        return self._modifier

    @property
    def name(self):
        """Returns name"""
        return self._name

    @property
    def value(self):
        """Returns value"""
        return self._value

    def apply(self, node: Node):
        """Applies option to passed node"""
        self._modifier(node, self._name, self._value)

    def __hash__(self):
        return hash((self._name, self._modifier))

    def __eq__(self, other):
        return hash(self) == hash(other)


class Style(Node):
    """Node for storing config options"""

    def __init__(self, xml_node: XmlNode, node_globals: InheritedDict = None):
        super().__init__(xml_node, node_globals)
        self.name = None
        self.items = {}
