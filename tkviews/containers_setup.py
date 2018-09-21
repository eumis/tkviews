'''
Contains methods for node setups creation
'''

from pyviews import Node, NodeSetup, get_view_root
from pyviews.core.ioc import SERVICES as deps
from pyviews.rendering.flow import apply_attributes, render_children
from tkviews.core.containers import View

def get_container_setup():
    '''Returns setup for container'''
    node_setup = NodeSetup(setter=setattr, get_child_args=_get_child_args)
    node_setup.render_steps = [
        apply_attributes,
        render_children
    ]
    return node_setup

def get_view_setup():
    '''Returns setup for container'''
    node_setup = NodeSetup(setter=setattr, get_child_args=_get_child_args)
    node_setup.render_steps = [
        apply_attributes,
        _render_view_children
    ]
    return node_setup

def _render_view_children(node: View, node_setup: NodeSetup, **args):
    child_args = node_setup.get_child_init_args(node, **args)
    view_root = get_view_root(node.name)
    node.set_content(deps.render(view_root, **child_args))

def _get_child_args(node: Node):
    return {
        'parent_node': node,
        'master': node.master,
        'node_globals': node.globals,
        'node_styles': node.styles
    }
