'''Geometry managers wrappers'''

from abc import ABC, abstractmethod
from pyviews.core.xml import XmlNode
from pyviews.core.node import Node

class Geometry(ABC):
    '''Base for wrapper'''
    def __init__(self, **args):
        self._args = args if args else {}

    def set(self, key, value):
        '''Sets geometry parameter'''
        self._args[key] = value

    @abstractmethod
    def apply(self, widget):
        '''Applies geomtery with passed parameters'''

    def forget(self, widget):
        '''Calls forget method for geometry'''

class GridGeometry(Geometry):
    '''Grid geometry wrapper'''
    def apply(self, widget):
        widget.grid(**self._args)

    def forget(self, widget):
        widget.grid_forget()

class PackGeometry(Geometry):
    '''Pack geometry wrapper'''
    def apply(self, widget):
        widget.pack(**self._args)

    def forget(self, widget):
        widget.pack_forget()

class PlaceGeometry(Geometry):
    '''Place geometry wrapper'''
    def apply(self, widget):
        widget.place(**self._args)

    def forget(self, widget):
        widget.place_forget()

class LayoutSetup(Node, ABC):
    '''Base for wrappers under methods calls of geometry'''
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(xml_node, parent_context)
        self._master = master
        self.args = {}
        self.index = None

    @abstractmethod
    def apply(self):
        '''Calls config with passed parameters'''

class Row(LayoutSetup):
    '''Wrapper under grid_rowconfigure method'''
    def apply(self):
        self._master.grid_rowconfigure(self.index, **self.args)

class Column(LayoutSetup):
    '''Wrapper under grid_columnconfigure method'''
    def apply(self):
        self._master.grid_columnconfigure(self.index, **self.args)
