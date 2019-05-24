"""Common modifiers"""

from sys import exc_info
from pyviews.core import CoreError
from tkviews.node import WidgetNode


class CallbackError(CoreError):
    """Error from callback"""

    def __init__(self, message, event, view_info=None):
        super().__init__(message, view_info)
        self.add_info('Event', event)


def bind(node: WidgetNode, event_name, command):
    """Calls widget node bind method"""
    command = _get_handled_command(command, node.xml_node.view_info, event_name)
    node.bind('<{0}>'.format(event_name), command)


def _get_handled_command(command, view_info, event):
    return lambda *args, **kwargs: _call_command(command, view_info, event, args, kwargs)


def _call_command(command, view_info, event, args, kwargs):
    try:
        command(*args, **kwargs)
    except CoreError as error:
        error.add_view_info(view_info)
        raise
    except:
        info = exc_info()
        raise CallbackError('Error occurred in callback', event, view_info) \
            from info[1]


def bind_all(node: WidgetNode, event_name, command):
    """Calls widget's bind_all method"""
    command = _get_handled_command(command, node.xml_node.view_info, event_name)
    node.bind_all(f'<{event_name}>', command)


def set_attr(node: WidgetNode, key, value):
    """Calls nodes's set_attr method"""
    node.set_attr(key, value)


def config(node: WidgetNode, key, value):
    """Calls widget's config method"""
    node.instance.config(**{key: value})


def visible(node: WidgetNode, _, value):
    """Changes widget visibility"""
    if value:
        node.geometry.apply(node.instance)
    else:
        node.geometry.forget(node.instance)
