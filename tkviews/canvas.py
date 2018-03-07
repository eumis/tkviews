'''Wrappers for canvas elements'''

from tkinter import Canvas, TclError
from pyviews.core import get_not_implemented_message
from pyviews.core.ioc import inject
from pyviews.core.node import Node

class CanvasNode(Node):
    '''Base class for wrappers'''
    def __init__(self, master: Canvas, xml_node, parent_context=None):
        super().__init__(xml_node, parent_context)
        self._canvas = master
        self.item_id = None
        self._rendered = False
        self._corner = None
        self._size = []
        self._place = None
        self._options = {}
        self._events = {}
        self._style = ''

    @property
    def place(self):
        '''Arguments passed to create function of canvas.'''
        return self._place

    @place.setter
    def place(self, value: tuple):
        self._place = value

    @property
    def style(self):
        '''Widget styles'''
        return self._style

    @style.setter
    @inject('apply_styles')
    def style(self, value: str, apply_styles=None):
        self._style = value
        apply_styles(self, value)

    def set_attr(self, key, value):
        '''Sets passed attribute as node property or as element config'''
        if hasattr(self, key):
            setattr(self, key, value)
        elif self._rendered:
            try:
                self._canvas.itemconfig(self.item_id, **{key: value})
            except TclError:
                pass
        else:
            self._options[key] = value

    def render(self):
        '''Creates canvas element'''
        self.item_id = self._create()
        for event, command in self._events.items():
            self._canvas.tag_bind(self.item_id, '<' + event + '>', command)

        self._events = None
        self._options = None
        self._rendered = True

    def _create(self):
        raise NotImplementedError(get_not_implemented_message(self, '_create'))

    def bind(self, event: str, command):
        '''Binds element to event'''
        if self._rendered:
            self._canvas.tag_bind(self.item_id, '<' + event + '>', command)
        else:
            self._events[event] = command

    def destroy(self):
        '''Removes element from canvas'''
        self._canvas.delete(self.item_id)

class Rectangle(CanvasNode):
    '''create_rectangle wrapper'''
    def _create(self):
        return self._canvas.create_rectangle(*self._place, **self._options)

class Text(CanvasNode):
    '''create_text wrapper'''
    def _create(self):
        return self._canvas.create_text(*self._place, **self._options)

class Image(CanvasNode):
    '''create_image wrapper'''
    def _create(self):
        return self._canvas.create_image(*self._place, **self._options)

class Arc(CanvasNode):
    '''create_arc wrapper'''
    def _create(self):
        return self._canvas.create_arc(*self._place, **self._options)

class Bitmap(CanvasNode):
    '''create_arc wrapper'''
    def _create(self):
        return self._canvas.create_bitmap(*self._place, **self._options)

class Line(CanvasNode):
    '''create_line wrapper'''
    def _create(self):
        return self._canvas.create_line(*self._place, **self._options)

class Oval(CanvasNode):
    '''create_oval wrapper'''
    def _create(self):
        return self._canvas.create_oval(*self._place, **self._options)

class Polygon(CanvasNode):
    '''create_polygon wrapper'''
    def _create(self):
        return self._canvas.create_polygon(*self._place, **self._options)

class Window(CanvasNode):
    '''create_window wrapper'''
    def _create(self):
        return self._canvas.create_window(*self._place, **self._options)

def render(node: CanvasNode):
    '''Calls node's render'''
    node.render()
