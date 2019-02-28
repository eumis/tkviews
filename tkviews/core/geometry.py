'''Geometry managers wrappers'''

from abc import ABC, abstractmethod

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
