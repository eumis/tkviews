"""Contains rendering steps for style nodes"""
from injectool import resolve
from pyviews.core import XmlAttr, InheritedDict, Expression
from pyviews.compilation import is_expression, parse_expression
from pyviews.rendering import get_setter, render_children, RenderingPipeline
from tkviews.node import Style, StyleItem, StyleError
from tkviews.rendering.common import TkRenderingContext


def get_style_setup() -> RenderingPipeline:
    """Returns setup for style node"""
    return RenderingPipeline([
        apply_style_items,
        apply_parent_items,
        store_to_node_styles,
        render_child_styles
        # remove_style_on_destroy
    ])


def apply_style_items(node: Style, _: TkRenderingContext):
    """Parsing step. Parses attributes to style items and sets them to style"""
    attrs = node.xml_node.attrs
    try:
        node.name = next(attr.value for attr in attrs if attr.name == 'name')
    except StopIteration:
        raise StyleError('Style name is missing', node.xml_node.view_info)
    node.items = {attr.name: _get_style_item(node, attr) for attr in attrs if attr.name != 'name'}


def _get_style_item(node: Style, attr: XmlAttr):
    setter = get_setter(attr)
    value = attr.value if attr.value else ''
    if is_expression(value):
        expression_ = resolve(Expression, parse_expression(value)[1])
        value = expression_.execute(node.node_globals.to_dictionary())
    return StyleItem(setter, attr.name, value)


def apply_parent_items(node: Style, context: TkRenderingContext):
    """Sets style items from parent style"""
    parent_name = context.get('parent_name', None)
    if parent_name:
        parent_items = context.node_styles[parent_name]
        node.items = {**parent_items, **node.items}


def store_to_node_styles(node: Style, context: TkRenderingContext):
    """Store styles to node styles"""
    context.node_styles[node.name] = node.items.values()


def render_child_styles(node: Style, context: TkRenderingContext):
    """Renders child styles"""
    child_context = TkRenderingContext()
    child_context.parent_node = node
    child_context['parent_name'] = node.name
    child_context.node_globals = InheritedDict(node.node_globals)
    child_context.node_styles = context.node_styles
    render_children(node, child_context)


def remove_style_on_destroy(node: Style, context: TkRenderingContext):
    """Removes style from styles on destroying"""
    context.node_styles.remove_key(node.name)
