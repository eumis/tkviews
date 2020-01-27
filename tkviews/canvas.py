"""Wrappers for canvas elements"""

from abc import ABC, abstractmethod
from tkinter import Canvas
from typing import Type, cast

from pyviews.core import XmlNode, InheritedDict, Node
from pyviews.pipes import apply_attributes
from pyviews.rendering import RenderingPipeline, RenderingError

from tkviews.core import TkNode
from tkviews.core.rendering import TkRenderingContext


class CanvasItemNode(Node, TkNode, ABC):
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


class Rectangle(CanvasItemNode):
    """create_rectangle wrapper"""

    def _create(self, **options):
        return self._canvas.create_rectangle(*self.place, **options)


class Text(CanvasItemNode):
    """create_text wrapper"""

    def _create(self, **options):
        return self._canvas.create_text(*self.place, **options)


class Image(CanvasItemNode):
    """create_image wrapper"""

    def _create(self, **options):
        return self._canvas.create_image(*self.place, **options)


class Arc(CanvasItemNode):
    """create_arc wrapper"""

    def _create(self, **options):
        return self._canvas.create_arc(*self.place, **options)


class Bitmap(CanvasItemNode):
    """create_arc wrapper"""

    def _create(self, **options):
        return self._canvas.create_bitmap(*self.place, **options)


class Line(CanvasItemNode):
    """create_line wrapper"""

    def _create(self, **options):
        return self._canvas.create_line(*self.place, **options)


class Oval(CanvasItemNode):
    """create_oval wrapper"""

    def _create(self, **options):
        return self._canvas.create_oval(*self.place, **options)


class Polygon(CanvasItemNode):
    """create_polygon wrapper"""

    def _create(self, **options):
        return self._canvas.create_polygon(*self.place, **options)


class Window(CanvasItemNode):
    """create_window wrapper"""

    def _create(self, **options):
        return self._canvas.create_window(*self.place, **options)


def get_canvas_pipeline(item_type: Type[CanvasItemNode]) -> RenderingPipeline:
    """Returns setup for canvas"""
    return RenderingPipeline(pipes=[
        setup_temp_setter,
        setup_temp_binding,
        apply_attributes,
        create_item,
        setup_config_setter,
        setup_event_binding,
        apply_temp_events,
        clear_temp
    ], create_node=lambda ctx: create_canvas_node(ctx, item_type))


def create_canvas_node(context: TkRenderingContext, node_type) -> Node:
    if not isinstance(context.master, Canvas):
        raise RenderingError(f'{node_type.__name__} parent should be Canvas')
    return node_type(cast(Canvas, context.master), context.xml_node, context.node_globals, context.node_styles)


def setup_temp_setter(node: CanvasItemNode, _: TkRenderingContext):
    """Stores attributes values to temp dictionary"""
    node.attr_values = {}
    node.attr_setter = _set_option_value


def _set_option_value(node: CanvasItemNode, key, value):
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node.attr_values[key] = value


def setup_temp_binding(node: CanvasItemNode, _: TkRenderingContext):
    """Stores event callbacks to temp dictionary"""
    node.events = {}
    node.bind_source = node.bind
    node.bind = lambda event, command, n=node: _bind(n, event, command)


def _bind(node: CanvasItemNode, event, command):
    node.events[event] = command


def create_item(node: CanvasItemNode, _: TkRenderingContext):
    """Calls canvas create_* method using temp attribute values"""
    node.create(node.attr_values)


def setup_config_setter(node: CanvasItemNode, _: TkRenderingContext):
    """Attribute values are passed to itemconfigure method"""
    node.attr_setter = _set_config_value


def _set_config_value(node: CanvasItemNode, key, value):
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node.config(**{key: value})


def setup_event_binding(node: CanvasItemNode, _: TkRenderingContext):
    """Binds created item to callbacks from temp dictionary"""
    node.bind = node.bind_source


def apply_temp_events(node: CanvasItemNode, _: TkRenderingContext):
    """Binds events from temp dictionary"""
    for event, command in node.events.items():
        node.bind(event, command)


def clear_temp(node: CanvasItemNode, _: TkRenderingContext):
    """Removes temps"""
    del node.attr_values
    del node.bind_source
    del node.events
