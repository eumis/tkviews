"""Contains methods for node setups creation"""

from pyviews.core import InheritedDict, render
from pyviews.rendering import RenderingPipeline, render_view
from pyviews.rendering import apply_attributes, render_children
from tkviews.node import Container, View, For, If


def get_container_setup() -> RenderingPipeline:
    """Returns setup for container"""
    node_setup = RenderingPipeline()
    node_setup.steps = [
        apply_attributes,
        render_container_children
    ]
    return node_setup


def render_container_children(node, **_):
    """Renders container children"""
    render_children(node, **_get_child_args(node))


def get_view_setup() -> RenderingPipeline:
    """Returns setup for container"""
    node_setup = RenderingPipeline()
    node_setup.steps = [
        apply_attributes,
        render_view_children,
        rerender_on_view_change
    ]
    return node_setup


def render_view_children(node: View, **_):
    """Finds view by name attribute and renders it as view node child"""
    if node.name:
        child_args = _get_child_args(node)
        content = render_view(node.name, **child_args)
        node.set_content(content)


def rerender_on_view_change(node: View, **args):
    """Subscribes to name change and renders new view"""
    node.name_changed = lambda n, val, old: _rerender_view(n, args) \
        if val != old else None


def _rerender_view(node: View, args: dict):
    node.destroy_children()
    render_view_children(node, **args)


def get_for_setup() -> RenderingPipeline:
    """Returns setup for For node"""
    node_setup = RenderingPipeline()
    node_setup.steps = [
        apply_attributes,
        render_for_items,
        rerender_on_items_change
    ]
    return node_setup


def render_for_items(node: For, **_):
    """Renders For children"""
    _render_for_children(node, node.items)


def _render_for_children(node: For, items: list, index_shift=0):
    item_xml_nodes = node.xml_node.children
    for index, item in enumerate(items):
        for xml_node in item_xml_nodes:
            child_args = _get_for_child_args(node, index + index_shift, item)
            child = render(xml_node, **child_args)
            node.add_child(child)


def _get_for_child_args(node: For, index, item):
    child_args = _get_child_args(node)
    child_globals = child_args['node_globals']
    child_globals['index'] = index
    child_globals['item'] = item
    child_args['node_globals'] = child_globals
    return child_args


def rerender_on_items_change(node: For, **args):
    """Subscribes to items change and updates children"""
    node.items_changed = lambda n, v, o: _on_items_changed(n, **args) \
        if v != o else None


def _on_items_changed(node: For, **_):
    _destroy_overflow(node)
    _update_existing(node)
    _create_not_existing(node)


def _destroy_overflow(node: For):
    try:
        items_count = len(node.items)
        children_count = len(node.xml_node.children) * items_count
        overflow = node.children[children_count:]
        for child in overflow:
            child.destroy()
        node._children = node.children[:children_count]
    except IndexError:
        pass


def _update_existing(node: For):
    item_children_count = len(node.xml_node.children)
    try:
        for index, item in enumerate(node.items):
            start = index * item_children_count
            end = (index + 1) * item_children_count
            for child_index in range(start, end):
                globs = node.children[child_index].node_globals
                globs['item'] = item
                globs['index'] = index
    except IndexError:
        pass


def _create_not_existing(node: For):
    item_children_count = len(node.xml_node.children)
    start = int(len(node.children) / item_children_count)
    end = len(node.items)
    items = [node.items[i] for i in range(start, end)]
    _render_for_children(node, items, start)


def get_if_setup() -> RenderingPipeline:
    """Returns setup for For node"""
    node_setup = RenderingPipeline()
    node_setup.steps = [
        apply_attributes,
        render_if,
        subscribe_to_condition_change
    ]
    return node_setup


def render_if(node: If, **_):
    """Renders children nodes if condition is true"""
    if node.condition:
        render_children(node, **_get_child_args(node))


def subscribe_to_condition_change(node: If, **args):
    """Renders if on condition change"""
    node.condition_changed = lambda n, v, o: _on_condition_change(n, v, o, **args)


def _on_condition_change(node: If, val: bool, old: bool, **args):
    if val == old:
        return
    node.destroy_children()
    render_if(node, **args)


def _get_child_args(node: Container):
    return {
        'parent_node': node,
        'master': node.master,
        'node_globals': InheritedDict(node.node_globals),
        'node_styles': node.node_styles
    }
