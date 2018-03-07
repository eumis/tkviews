'''Geometry managers wrappers'''

from pyviews.core import get_not_implemented_message
from pyviews.core.xml import XmlNode
from pyviews.core.node import Node
from pyviews.rendering.core import apply_attributes

class Geometry:
    '''Base for wrapper'''
    def __init__(self, **args):
        self._args = args if args else {}

    def set(self, key, value):
        '''Sets geometry parameter'''
        self._args[key] = value

    def apply(self, widget):
        '''Applies geomtery with passed parameters'''
        raise NotImplementedError(get_not_implemented_message(self, 'apply'))

    def forget(self, widget):
        '''Calls forget method for geometry'''
        pass

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

class LayoutSetup(Node):
    '''Base for wrappers under methods calls of geometry'''
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(xml_node, parent_context)
        self._master = master
        self._args = {}
        self._index = None

    def set_attr(self, key, value):
        '''Sets config parameter'''
        if key == 'index':
            self._index = value
        else:
            self._args[key] = value

    def apply(self):
        '''Calls config with passed parameters'''
        raise NotImplementedError(get_not_implemented_message(self, 'apply'))

class Row(LayoutSetup):
    '''Wrapper under grid_rowconfigure method'''
    def apply(self):
        self._master.grid_rowconfigure(self._index, **self._args)

class Column(LayoutSetup):
    '''Wrapper under grid_columnconfigure method'''
    def apply(self):
        self._master.grid_columnconfigure(self._index, **self._args)

def apply_layout(layout: LayoutSetup):
    '''Parsing step for LayoutSetup. Parses attributes and calls apply'''
    apply_attributes(layout)
    layout.apply()
