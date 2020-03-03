"""Common setters for widgets nodes"""

from tkinter import Event

from pyviews.core import PyViewsError
from pyviews.core import error_handling, ViewInfo

from tkviews.widgets.node import WidgetNode


class CallbackError(PyViewsError):
    """Error from callback"""


def bind(node: WidgetNode, event_name, command):
    """Calls widget node bind method"""
    command = _get_handled_command(command, node.xml_node.view_info, event_name)
    node.bind('<{0}>'.format(event_name), command)


def _get_handled_command(command, view_info, event):
    return lambda *args, **kwargs: _call_command(command, view_info, event, args, kwargs)


def _call_command(command, view_info, event, args, kwargs):
    with error_handling(CallbackError, lambda e: _add_callback_info(event, view_info, e)):
        command(*args, **kwargs)


def _add_callback_info(event: Event, view_info: ViewInfo, error: PyViewsError):
    error.add_view_info(view_info)
    error.add_info('Event', event)


def bind_all(node: WidgetNode, event_name, command):
    """Calls widget's bind_all method"""
    command = _get_handled_command(command, node.xml_node.view_info, event_name)
    node.bind_all(f'<{event_name}>', command)


def config(node: WidgetNode, key, value):
    """Calls widget's config method"""
    node.instance.config(**{key: value})
