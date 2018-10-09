'''
Contains methods for node setups creation
'''

from pyviews import NodeSetup
from pyviews.rendering.flow import apply_attributes
from tkviews.core.canvas import CanvasNode

def get_canvas_setup() -> NodeSetup:
    '''Returns setup for canvas'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        _setup_options_setter,
        _setup_local_events,
        apply_attributes,
        _create_item,
        _setup_config_setter,
        _setup_event_binding
    ]
    return node_setup

def _setup_options_setter(node: CanvasNode, **args):
    node._attr_values = {}
    node.setter = _set_option_value

def _set_option_value(node: CanvasNode, key, value):
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node._attr_values[key] = value

def _setup_local_events(node: CanvasNode, **args):
    node._events = {}
    node._bind_source = node.bind
    node.bind = lambda event, command, n=node: _bind(n, event, command)

def _bind(node: CanvasNode, event, command):
    node._events[event] = command

def _create_item(node: CanvasNode, **args):
    node.create(node._attr_values)

def _setup_config_setter(node: CanvasNode, **args):
    node.setter = _set_config_value

def _set_config_value(node: CanvasNode, key, value):
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node.config(**{key: value})

def _setup_event_binding(node: CanvasNode, **args):
    node.bind = node._bind_source
    for event, command in node._events.items():
        node.bind(event, command)
    node._bind_source = None
    node._events = None
