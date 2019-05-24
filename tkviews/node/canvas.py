"""Wrappers for canvas elements"""

from abc import ABC, abstractmethod
from tkinter import Canvas
from pyviews.core import XmlNode, InheritedDict, Node
from tkviews.core import TkNode


class CanvasNode(Node, TkNode, ABC):
    """Base class for wrappers"""

    def __init__(self, master: Canvas, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self._canvas = master
        self._item_id = None
        self._node_styles = node_styles
        self.place = []

    @property
    def item_id(self):
        """id returned from create method of canvas"""
        return self._item_id

    @property
    def node_styles(self):
        """Returns node_styles"""
        return self._node_styles

    def create(self, **options):
        """Creates canvas element"""
        self._item_id = self._create(**options)

    @abstractmethod
    def _create(self, **options):
        pass

    def bind(self, event: str, command):
        """Binds element to event"""
        self._canvas.tag_bind(self.item_id, '<' + event + '>', command)

    def config(self, **options):
        """Calls itemconfig of canvas"""
        self._canvas.itemconfig(self.item_id, **options)

    def destroy(self):
        """Removes element from canvas"""
        self._canvas.delete(self.item_id)


class Rectangle(CanvasNode):
    """create_rectangle wrapper"""

    def _create(self, **options):
        return self._canvas.create_rectangle(*self.place, **options)


class Text(CanvasNode):
    """create_text wrapper"""

    def _create(self, **options):
        return self._canvas.create_text(*self.place, **options)


class Image(CanvasNode):
    """create_image wrapper"""

    def _create(self, **options):
        return self._canvas.create_image(*self.place, **options)


class Arc(CanvasNode):
    """create_arc wrapper"""

    def _create(self, **options):
        return self._canvas.create_arc(*self.place, **options)


class Bitmap(CanvasNode):
    """create_arc wrapper"""

    def _create(self, **options):
        return self._canvas.create_bitmap(*self.place, **options)


class Line(CanvasNode):
    """create_line wrapper"""

    def _create(self, **options):
        return self._canvas.create_line(*self.place, **options)


class Oval(CanvasNode):
    """create_oval wrapper"""

    def _create(self, **options):
        return self._canvas.create_oval(*self.place, **options)


class Polygon(CanvasNode):
    """create_polygon wrapper"""

    def _create(self, **options):
        return self._canvas.create_polygon(*self.place, **options)


class Window(CanvasNode):
    """create_window wrapper"""

    def _create(self, **options):
        return self._canvas.create_window(*self.place, **options)
