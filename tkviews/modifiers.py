'''Common modifiers'''

from tkviews.widgets import WidgetNode

def bind(node: WidgetNode, event_name, command):
    '''Calls widget's bind method'''
    node.bind(event_name, command)

def bind_all(node: WidgetNode, event_name, command):
    '''Calls widget's bind_all method'''
    node.bind_all(event_name, command)

def set_attr(node: WidgetNode, key, value):
    '''Calls nodes's set_attr method'''
    node.set_attr(key, value)

def config(node: WidgetNode, key, value):
    '''Calls widget's config method'''
    node.widget.config(**{key: value})

def visible(node: WidgetNode, key, value):
    '''Changes widget visibility'''
    if value:
        node.geometry.apply(node.widget)
    else:
        node.geometry.forget(node.widget)
