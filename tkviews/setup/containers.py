'''
Contains methods for node setups creation
'''

from pyviews import Node, NodeSetup, get_view_root
from pyviews.core.ioc import SERVICES as deps
from pyviews.core.observable import InheritedDict
from pyviews.rendering.flow import apply_attributes, render_children
from tkviews.core.containers import View, For, If

def get_container_setup() -> NodeSetup:
    '''Returns setup for container'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        apply_attributes,
        render_children
    ]
    node_setup.get_child_args = _get_child_args
    return node_setup

def get_view_setup() -> NodeSetup:
    '''Returns setup for container'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        apply_attributes,
        _render_view_children
    ]
    node_setup.get_child_args = _get_child_args
    return node_setup

def _render_view_children(node: View, node_setup: NodeSetup = None, **args):
    child_args = node_setup.get_child_init_args(node, **args)
    view_root = get_view_root(node.name)
    node.set_content(deps.render(view_root, **child_args))

def get_for_setup() -> NodeSetup:
    '''Returns setup for For node'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        apply_attributes,
        _subscribe_to_items_change,
        _render_for
    ]
    node_setup.get_child_args = _get_child_args
    return node_setup

def _subscribe_to_items_change(node: For, node_setup: NodeSetup, **args):
    node.items_observable.callback = lambda n, v, o, ns=node_setup: _on_items_changed(n, ns)

def _on_items_changed(node: For, node_setup: NodeSetup):
    _destroy_overflow(node)
    _update_existing(node)
    _create_not_existing(node, node_setup)

def _destroy_overflow(node: For):
    try:
        items_count = len(node.items)
        children_count = len(node.xml_node.children) * items_count
        overflow = node._children[children_count:]
        for child in overflow:
            child.destroy()
        node._children = node._children[:children_count]
    except IndexError:
        pass

def _update_existing(node: For):
    item_children_count = len(node.xml_node.children)
    try:
        for index, item in enumerate(node.items):
            start = index * item_children_count
            end = (index + 1) * item_children_count
            for child_index in range(start, end):
                globs = node._children[child_index].globals
                globs['item'] = item
    except IndexError:
        pass

def _create_not_existing(node: For, node_setup: NodeSetup):
    item_children_count = len(node.xml_node.children)
    start = int(len(node._children) / item_children_count)
    end = len(node.items)
    items = [node.items[i] for i in range(start, end)]
    _render_for_children(node, node_setup, items)

def _render_for_children(node: For, node_setup: NodeSetup, items: list):
    item_xml_nodes = node.xml_node.children
    for index, item in enumerate(items):
        for xml_node in item_xml_nodes:
            child_args = _get_for_child_args(node_setup, node, index, item)
            child = deps.render(xml_node, **child_args)
            node.add_child(child)
    _render_for_children(node, node_setup, node.items)

def _get_for_child_args(node: For, node_setup: NodeSetup, index, item):
    child_args = node_setup.get_render_args(node)
    child_globals = InheritedDict(child_args['node_globals'])
    child_globals['index'] = index
    child_globals['item'] = item
    child_args['node_globals'] = child_globals
    return child_args

def _render_for(node: For, node_setup: NodeSetup = None, **args):
    node.destroy_children()
 
def get_if_setup() -> NodeSetup:
    '''Returns setup for For node'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        apply_attributes,
        _subscribe_to_condition_change,
        _render_if
    ]
    node_setup.get_child_args = _get_child_args
    return node_setup

def _subscribe_to_condition_change(node: If, node_setup: NodeSetup = None, **args):
    node.condition_observable.callback = lambda n, v, o, ns=NodeSetup: _on_condition_change(n, ns, v, o, **args)

def _on_condition_change(node: If, node_setup: NodeSetup, val: bool, old: bool, **args):
    if val == old:
        return
    node.destroy_children()
    _render_if(node, node_setup, **args)

def _render_if(node: If, node_setup: NodeSetup = None, **args):
    if node.condition:
        render_children(node, node_setup=node_setup, **args)

def _get_child_args(node: Node):
    return {
        'parent_node': node,
        'master': node.master,
        'node_globals': node.globals,
        'node_styles': node.styles
    }
