"""Contains methods for node setups creation"""

from pyviews.rendering import RenderingPipeline, apply_attributes
from tkviews.node import CanvasNode


def get_canvas_setup() -> RenderingPipeline:
    """Returns setup for canvas"""
    return RenderingPipeline(steps=[
        setup_temp_setter,
        setup_temp_binding,
        apply_attributes,
        create_item,
        setup_config_setter,
        setup_event_binding,
        apply_temp_events,
        clear_temp
    ])


def setup_temp_setter(node: CanvasNode, **_):
    """Stores attributes values to temp dictionary"""
    node.attr_values = {}
    node.attr_setter = _set_option_value


def _set_option_value(node: CanvasNode, key, value):
    if key in node.properties:
        node.properties[key].set_value(value)
    elif hasattr(node, key):
        setattr(node, key, value)
    else:
        node.attr_values[key] = value


def setup_temp_binding(node: CanvasNode, **_):
    """Stores event callbacks to temp dictionary"""
    node.events = {}
    node.bind_source = node.bind
    node.bind = lambda event, command, n=node: _bind(n, event, command)


def _bind(node: CanvasNode, event, command):
    node.events[event] = command


def create_item(node: CanvasNode, **_):
    """Calls canvas create_* method using temp attribute values"""
    node.create(node.attr_values)


def setup_config_setter(node: CanvasNode, **_):
    """Attribute values are passed to itemconfigure method"""
    node.attr_setter = _set_config_value


def _set_config_value(node: CanvasNode, key, value):
    if key in node.properties:
        node.properties[key].set_value(value)
    elif hasattr(node, key):
        setattr(node, key, value)
    else:
        node.config(**{key: value})


def setup_event_binding(node: CanvasNode, **_):
    """Binds created item to callbacks from temp dictionary"""
    node.bind = node.bind_source


def apply_temp_events(node: CanvasNode, **_):
    """Binds events from temp dictionary"""
    for event, command in node.events.items():
        node.bind(event, command)


def clear_temp(node: CanvasNode, **_):
    """Removes temps"""
    del node.attr_values
    del node.bind_source
    del node.events
