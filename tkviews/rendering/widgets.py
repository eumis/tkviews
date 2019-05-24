"""Contains rendering setup for widget nodes"""

from pyviews.core import XmlAttr, Node, Property, InheritedDict
from pyviews.rendering import RenderingPipeline, apply_attributes, render_children, apply_attribute
from tkviews.core.geometry import Geometry
from tkviews.node import WidgetNode, StyleError


def get_root_setup():
    """Returns setup for root"""
    node_setup = RenderingPipeline()
    node_setup.steps = [
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        render_widget_children
    ]
    return node_setup


def setup_widget_setter(node: Node, **_):
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


def setup_widget_destroy(node: WidgetNode, **_):
    """Sets up on destroy method"""
    node.on_destroy = _on_widget_destroy


def _on_widget_destroy(node: WidgetNode):
    node.instance.destroy()


def render_widget_children(node: WidgetNode, **_):
    """Renders child widgets"""
    render_children(node,
                    parent_node=node,
                    master=node.instance,
                    node_globals=InheritedDict(node.node_globals),
                    node_styles=node.node_styles)


def get_widget_setup():
    """Returns setup for widget"""
    node_setup = RenderingPipeline()
    node_setup.steps = [
        setup_properties,
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        apply_text,
        render_widget_children
    ]
    return node_setup


def setup_properties(node: WidgetNode, **_):
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


def apply_text(node: WidgetNode, **_):
    """Applies xml node content to WidgetNode"""
    if node.xml_node.text is None or not node.xml_node.text.strip():
        return
    text_attr = XmlAttr('text', node.xml_node.text)
    apply_attribute(node, text_attr)
