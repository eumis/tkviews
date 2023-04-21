"""Tkinter widgets nodes"""
from functools import partial
from tkinter import PanedWindow, Tk, Widget
from typing import Optional

from pyviews.core.rendering import InstanceNode, NodeGlobals
from pyviews.core.xml import XmlAttr, XmlNode
from pyviews.pipes import apply_attribute, apply_attributes, render_children
from pyviews.rendering.pipeline import RenderingPipeline, create_instance, get_type

from tkviews.core import TkRenderingContext


class Root(InstanceNode):
    """Wrapper under tkinter Root"""

    def __init__(self, xml_node: XmlNode, node_globals: Optional[NodeGlobals] = None):
        super().__init__(Tk(), xml_node, node_globals)
        self._icon = None

    @property
    def state(self):
        """Widget state"""
        return self.instance.state()

    @state.setter
    def state(self, state):
        self.instance.state(state)

    @property
    def icon(self):
        """Icon path"""
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.instance.iconbitmap(default = value)

    def bind(self, event, command):
        """Calls widget bind"""
        self.instance.bind(event, command)

    def bind_all(self, event, command):
        """Calls widget bind"""
        self.instance.bind_all(event, command)


def get_root_pipeline() -> RenderingPipeline:
    """Returns setup for root"""
    return RenderingPipeline(pipes=[
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        render_widget_children
    ], name='root pipeline') # yapf: disable


class WidgetNode(InstanceNode):
    """Wrapper under tkinter widget"""

    def __init__(self, widget: Widget, xml_node: XmlNode, node_globals: Optional[NodeGlobals] = None):
        super().__init__(widget, xml_node, node_globals = node_globals)

    def bind(self, event, command):
        """Calls widget bind"""
        self.instance.bind(event, command)

    def bind_all(self, event, command):
        """Calls widget bind"""
        self.instance.bind_all(event, command)


def get_widget_pipeline() -> RenderingPipeline:
    """Returns setup for widget"""
    return RenderingPipeline(pipes=[
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        apply_text,
        add_to_panedwindow,
        render_widget_children
    ], create_node=_create_widget_node, name='widget pipeline') # yapf: disable


def setup_widget_setter(node: WidgetNode, _: TkRenderingContext):
    """Sets up setter"""
    node.set_attr = partial(_widget_node_setter, node)


def _widget_node_setter(node: WidgetNode, key: str, value):
    """Applies passed attribute"""
    if key == 'ttkstyle':
        pass
    if hasattr(node, key):
        setattr(node, key, value)
    elif hasattr(node.instance, key):
        setattr(node.instance, key, value)
    else:
        node.instance.configure(**{key: value})


def setup_widget_destroy(node: WidgetNode, _: TkRenderingContext):
    """Sets up on destroy method"""
    node.on_destroy = _on_widget_destroy


def _on_widget_destroy(node: WidgetNode):
    node.instance.destroy()


def render_widget_children(node: WidgetNode, context: TkRenderingContext):
    """Render step. Renders widget children"""
    render_children(node, context, _get_child_context)


def _get_child_context(xml_node: XmlNode, node: WidgetNode, _: TkRenderingContext):
    """Renders child widgets"""
    child_context = TkRenderingContext()
    child_context.xml_node = xml_node
    child_context.parent_node = node
    child_context.master = node.instance
    child_context.node_globals = NodeGlobals(node.node_globals)
    return child_context


def _create_widget_node(context: TkRenderingContext):
    inst_type = get_type(context.xml_node)
    inst = create_instance(inst_type, context)
    return create_instance(WidgetNode, {'widget': inst, **context})


def apply_text(node: WidgetNode, _: TkRenderingContext):
    """Applies xml node content to WidgetNode"""
    if node.xml_node.text is None or not node.xml_node.text.strip():
        return
    text_attr = XmlAttr('text', node.xml_node.text)
    apply_attribute(node, text_attr)


def add_to_panedwindow(node: WidgetNode, context: TkRenderingContext):
    """Sets up setter"""
    if isinstance(context.master, PanedWindow):
        context.master.add(node.instance)
