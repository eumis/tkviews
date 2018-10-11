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
        setup_temp_setter,
        setup_temp_binding,
        apply_attributes,
        create_item,
        setup_config_setter,
        setup_event_binding,
        apply_temp_events,
        clear_temp
    ]
    return node_setup

# pylint: disable=W0613

def setup_temp_setter(node: CanvasNode, **args):
    '''Stores attributes values to temp dictionary'''
    node.attr_values = {}
    node.setter = _set_option_value

def _set_option_value(node: CanvasNode, key, value):
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node.attr_values[key] = value

def setup_temp_binding(node: CanvasNode, **args):
    '''Stores event callbacks to temp dictionary'''
    node.events = {}
    node.bind_source = node.bind
    node.bind = lambda event, command, n=node: _bind(n, event, command)

def _bind(node: CanvasNode, event, command):
    node.events[event] = command

def create_item(node: CanvasNode, **args):
    '''Calls canvas create_* method using temp attribute values'''
    node.create(node.attr_values)

def setup_config_setter(node: CanvasNode, **args):
    '''Attribute values are passed to itemconfigure method'''
    node.setter = _set_config_value

def _set_config_value(node: CanvasNode, key, value):
    node.config(**{key: value})

def setup_event_binding(node: CanvasNode, **args):
    '''Binds created item to callbacks from temp dictionary'''
    node.bind = node.bind_source

def apply_temp_events(node: CanvasNode, **args):
    '''Binds events from temp dictionary'''
    for event, command in node.events.items():
        node.bind(event, command)

def clear_temp(node: CanvasNode, **args):
    '''Removes temps'''
    del node.attr_values
    del node.bind_source
    del node.events
