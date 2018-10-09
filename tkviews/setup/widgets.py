'''Contains rendering setup for widget nodes'''

from pyviews import Node, NodeSetup
from pyviews.core.xml import XmlAttr
from pyviews.core.ioc import inject
from pyviews.core.node import Property
from pyviews.rendering.flow import apply_attributes, render_children, apply_attribute
from tkviews.core.geometry import Geometry
from tkviews.core.widgets import WidgetNode

def get_root_setup():
    '''Returns setup for root'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        render_children
    ]
    node_setup.get_child_args = _get_child_args
    return node_setup

def setup_widget_setter(node: Node, **args):
    '''Sets up setter'''
    node.setter = _widget_node_setter

def _widget_node_setter(node: WidgetNode, key: str, value):
    '''Applies passed attribute'''
    if hasattr(node, key):
        setattr(node, key, value)
    elif hasattr(node.instance, key):
        setattr(node.instance, key, value)
    else:
        node.instance.configure(**{key:value})

def setup_widget_destroy(node: WidgetNode, **args):
    '''Sets up on destroy method'''
    node.on_destroy = _on_widget_destroy

def _on_widget_destroy(node: WidgetNode):
    node.instance.destroy()

def get_widget_setup():
    '''Returns setup for widget'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        setup_properties,
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        render_children
    ]
    node_setup.properties = {
        'geometry': Property('geometry', _geometry_setter),
        'style': Property('style', _style_setter)
    }
    node_setup.get_child_args = _get_child_args
    node_setup.on_destroy = _on_widget_destroy

def setup_properties(node: WidgetNode, **args):
    '''Sets up widget node properties'''
    node.properties['geometry']: Property('geometry', _geometry_setter)
    node.properties['style']: Property('style', _style_setter)

def _geometry_setter(node: WidgetNode, geometry: Geometry, previous: Geometry):
    if previous:
        previous.forget()
    if geometry is not None:
        geometry.apply(node.instance)
    return geometry

@inject('apply_styles')
def _style_setter(node: WidgetNode, styles: str, apply_styles=None):
    apply_styles(node, styles)
    return styles

def apply_text(node: WidgetNode):
    '''Applies xml node content to WidgetNode'''
    if node.xml_node.text is None or not node.xml_node.text.strip():
        return
    text_attr = XmlAttr('text', node.xml_node.text)
    apply_attribute(node, text_attr)

def _get_child_args(node: WidgetNode):
    return {
        'parent_node': node,
        'master': node.instance,
        'node_globals': node.globals,
        'node_styles': node.node_styles
    }