"""Nodes for storing config options for widgets"""

from typing import Any, Union, List

from pyviews.core import PyViewsError, XmlNode, Node, InheritedDict, Setter, XmlAttr
from pyviews.pipes import render_children
from pyviews.rendering import RenderingPipeline

from tkviews.core import TkRenderingContext, render_attribute
from tkviews.widgets import WidgetNode


class StyleError(PyViewsError):
    """Error for style"""


class StyleItem:
    """Wrapper under option"""

    def __init__(self, setter: Setter, name: str, value: Any):
        self._setter = setter
        self._name = name
        self._value = value

    @property
    def setter(self):
        """Returns setter"""
        return self._setter

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
        self._setter(node, self._name, self._value)

    def __hash__(self):
        return hash((self._name, self._setter))

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
        lambda style, ctx: render_children(style, ctx, _get_style_child_context)
    ])


def apply_style_items(node: Style, _: TkRenderingContext):
    """Parsing step. Parses attributes to style items and sets them to style"""
    attrs = node.xml_node.attrs
    try:
        node.name = next(attr.value for attr in attrs if attr.name == 'name')
    except StopIteration:
        raise StyleError('Style name is missing', node.xml_node.view_info)
    node.items = {attr.name: _get_style_item(node, attr) for attr in attrs if attr.name != 'name'}


def _get_style_item(node: Style, xml_attr: XmlAttr):
    setter, value = render_attribute(node, xml_attr)
    return StyleItem(setter, xml_attr.name, value)


def apply_parent_items(node: Style, context: TkRenderingContext):
    """Sets style items from parent style"""
    parent_name = context.get('parent_name', None)
    if parent_name:
        parent_items = context.node_styles[parent_name]
        node.items = {**parent_items, **node.items}


def store_to_node_styles(node: Style, context: TkRenderingContext):
    """Store styles to node styles"""
    context.node_styles[node.name] = node.items.values()


def _get_style_child_context(xml_node: XmlNode, node: Style,
                             context: TkRenderingContext) -> TkRenderingContext:
    """Renders child styles"""
    child_context = TkRenderingContext()
    child_context.xml_node = xml_node
    child_context.parent_node = node
    child_context['parent_name'] = node.name
    child_context.node_globals = InheritedDict(node.node_globals)
    child_context.node_styles = context.node_styles
    return child_context


def apply_styles(node: WidgetNode, _: str, style_keys: Union[str, List[str]]):
    """Setter. Applies styles to node"""
    if not style_keys:
        return
    try:
        _apply_styles(node, style_keys)
    except KeyError as key_error:
        error = StyleError('Style is not found')
        error.add_info('Style name', key_error.args[0])
        raise error from key_error


def _apply_styles(node, style_keys: Union[str, List[str]]):
    keys = [key.strip() for key in style_keys.split(',')] \
        if isinstance(style_keys, str) else style_keys
    for key in [key for key in keys if key]:
        for item in node.node_styles[key]:
            item.apply(node)
