"""Contains rendering setup for widget nodes"""

from pyviews.core import XmlAttr, Node, Property, InheritedDict
from pyviews.rendering import RenderingPipeline, apply_attributes, render_children, apply_attribute

from tkviews.core.geometry import Geometry
from tkviews.node import WidgetNode, StyleError
from tkviews.rendering.common import TkRenderingContext


def get_root_setup():
    """Returns setup for root"""
    return RenderingPipeline([
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        render_widget_children
    ])


def setup_widget_setter(node: Node, _: TkRenderingContext):
    """Sets up setter"""
    node.attr_setter = _widget_node_setter


def _widget_node_setter(node: WidgetNode, key: str, value):
    """Applies passed attribute"""
    if key in node.properties:
        node.properties[key].set(value)
    elif hasattr(node, key):
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


def render_widget_children(node: WidgetNode, _: TkRenderingContext):
    """Renders child widgets"""
    child_context = TkRenderingContext()
    child_context.parent_node = node
    child_context.master = node.instance
    child_context.node_globals = InheritedDict(node.node_globals)
    child_context.node_styles = node.node_styles
    render_children(node, child_context)


def get_widget_setup():
    """Returns setup for widget"""
    return RenderingPipeline([
        setup_properties,
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        apply_text,
        render_widget_children
    ])


def setup_properties(node: WidgetNode, _: TkRenderingContext):
    """Sets up widget node properties"""
    node.properties['geometry'] = Property('geometry', _geometry_setter, node=node)
    node.properties['style'] = Property('style', _style_setter, node=node)


def _geometry_setter(node: WidgetNode, geometry: Geometry, previous: Geometry):
    if previous:
        previous.forget(node.instance)
    if geometry is not None:
        geometry.apply(node.instance)
    return geometry


def _style_setter(node: WidgetNode, styles: str):
    apply_styles(node, styles)
    return styles


def apply_styles(node: WidgetNode, style_keys: str):
    """Applies styles to node"""
    keys = [key.strip() for key in style_keys.split(',')] \
        if isinstance(style_keys, str) else style_keys
    try:
        for key in [key for key in keys if key]:
            for item in node.node_styles[key]:
                item.apply(node)
    except KeyError as key_error:
        error = StyleError('Style is not found')
        error.add_info('Style name', key_error.args[0])
        raise error from key_error


def apply_text(node: WidgetNode, _: TkRenderingContext):
    """Applies xml node content to WidgetNode"""
    if node.xml_node.text is None or not node.xml_node.text.strip():
        return
    text_attr = XmlAttr('text', node.xml_node.text)
    apply_attribute(node, text_attr)
