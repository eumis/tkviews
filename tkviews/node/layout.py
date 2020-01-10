"""Layout nodes"""

from abc import ABC, abstractmethod
from pyviews.core.xml import XmlNode
from pyviews.core.node import Node


class LayoutSetup(Node, ABC):
    """Base for wrappers under methods calls of geometry"""

    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(xml_node, parent_context)
        self._master = master
        self.args = {}
        self.index = None

    def set_attr(self, key, value):
        """Sets config parameter"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.args[key] = value

    @abstractmethod
    def apply(self):
        """Calls config with passed parameters"""


class Row(LayoutSetup):
    """Wrapper under grid_rowconfigure method"""

    def apply(self):
        self._master.grid_rowconfigure(self.index, **self.args)


class Column(LayoutSetup):
    """Wrapper under grid_columnconfigure method"""

    def apply(self):
        self._master.grid_columnconfigure(self.index, **self.args)
