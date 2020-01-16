"""Nodes for storing config options for widgets"""

from typing import Any

from pyviews.compilation import is_expression, Expression, parse_expression
from pyviews.core import ViewsError, XmlNode, Node, InheritedDict, Modifier, XmlAttr
from pyviews.pipes import render_children, get_setter
from pyviews.rendering import RenderingPipeline

from tkviews.core.common import TkRenderingContext


class StyleError(ViewsError):
    """Error for style"""


class StyleItem:
    """Wrapper under option"""

    def __init__(self, modifier: Modifier, name: str, value: Any):
        self._modifier = modifier
        self._name = name
        self._value = value

    @property
    def setter(self):
        """Returns setter"""
        return self._modifier

    @property
    def name(self):
        """Returns name"""
        return self._name

    @property
    def value(self):
        """Returns value"""
        return self._value

    def apply(self, node: Node):
        """Applies option to passed node"""
        self._modifier(node, self._name, self._value)

    def __hash__(self):
        return hash((self._name, self._modifier))

    def __eq__(self, other):
        return hash(self) == hash(other)


class Style(Node):
    """Node for storing config options"""

    def __init__(self, xml_node: XmlNode, node_globals: InheritedDict = None):
        super().__init__(xml_node, node_globals)
        self.name = None
        self.items = {}


def get_style_setup() -> RenderingPipeline:
    """Returns setup for style node"""
    return RenderingPipeline(pipes=[
        apply_style_items,
        apply_parent_items,
        store_to_node_styles,
        lambda style, ctx: render_children(style, ctx, _get_style_child_context),
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
        expression_ = Expression(parse_expression(value)[1])
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


def _get_style_child_context(xml_node: XmlNode, node: Style, context: TkRenderingContext) -> TkRenderingContext:
    """Renders child styles"""
    child_context = TkRenderingContext()
    child_context.xml_node = xml_node
    child_context.parent_node = node
    child_context['parent_name'] = node.name
    child_context.node_globals = InheritedDict(node.node_globals)
    child_context.node_styles = context.node_styles
    return child_context


def remove_style_on_destroy(node: Style, context: TkRenderingContext):
    """Removes style from styles on destroying"""
    context.node_styles.remove_key(node.name)
