"""Contains methods for node setups creation"""

from pyviews.core import InheritedDict
from pyviews.rendering import RenderingPipeline, render_view, render
from pyviews.rendering import apply_attributes, render_children
from tkviews.node import Container, View, For, If
from tkviews.rendering.common import TkRenderingContext


def get_container_setup() -> RenderingPipeline:
    """Returns setup for container"""
    return RenderingPipeline([
        apply_attributes,
        render_container_children
    ])


def render_container_children(node, _: TkRenderingContext):
    """Renders container children"""
    render_children(node, _get_child_context(node))


def get_view_setup() -> RenderingPipeline:
    """Returns setup for container"""
    return RenderingPipeline([
        apply_attributes,
        render_view_children,
        rerender_on_view_change
    ])


def render_view_children(node: View, _: TkRenderingContext):
    """Finds view by name attribute and renders it as view node child"""
    if node.name:
        child_context = _get_child_context(node)
        content = render_view(node.name, child_context)
        node.set_content(content)


def rerender_on_view_change(node: View, context: TkRenderingContext):
    """Subscribes to name change and renders new view"""
    node.name_changed = lambda n, val, old: _rerender_view(n, context) \
        if val != old else None


def _rerender_view(node: View, context: TkRenderingContext):
    node.destroy_children()
    render_view_children(node, context)


def get_for_setup() -> RenderingPipeline:
    """Returns setup for For node"""
    return RenderingPipeline([
        apply_attributes,
        render_for_items,
        rerender_on_items_change
    ])


def render_for_items(node: For, _: TkRenderingContext):
    """Renders For children"""
    _render_for_children(node, node.items)


def _render_for_children(node: For, items: list, index_shift=0):
    item_xml_nodes = node.xml_node.children
    for index, item in enumerate(items):
        for xml_node in item_xml_nodes:
            item_context = _get_for_child_args(node, index + index_shift, item)
            child = render(xml_node, item_context)
            node.add_child(child)


def _get_for_child_args(node: For, index, item) -> TkRenderingContext:
    child_context = _get_child_context(node)
    child_globals = child_context.node_globals
    child_globals['index'] = index
    child_globals['item'] = item
    child_context.node_globals = child_globals
    return child_context


def rerender_on_items_change(node: For, context: TkRenderingContext):
    """Subscribes to items change and updates children"""
    node.items_changed = lambda n, v, o: _on_items_changed(n, context) \
        if v != o else None


def _on_items_changed(node: For, _: TkRenderingContext):
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
    return RenderingPipeline([
        apply_attributes,
        render_if,
        subscribe_to_condition_change
    ])


def render_if(node: If, _: TkRenderingContext):
    """Renders children nodes if condition is true"""
    if node.condition:
        render_children(node, _get_child_context(node))


def subscribe_to_condition_change(node: If, context: TkRenderingContext):
    """Renders if on condition change"""
    node.condition_changed = lambda n, v, o: _on_condition_change(n, v, o, context)


def _on_condition_change(node: If, val: bool, old: bool, context: TkRenderingContext):
    if val == old:
        return
    node.destroy_children()
    render_if(node, context)


def _get_child_context(node: Container):
    return TkRenderingContext({
        'parent_node': node,
        'master': node.master,
        'node_globals': InheritedDict(node.node_globals),
        'node_styles': node.node_styles
    })
