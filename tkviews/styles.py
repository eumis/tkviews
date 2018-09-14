'''Nodes for storing config options for widgets'''

from typing import Any, Callable, List
from pyviews.core import CoreError
from pyviews.core.xml import XmlAttr, XmlNode
from pyviews.core.compilation import Expression
from pyviews.core.node import Node
from pyviews.core.observable import InheritedDict
from pyviews.rendering.flow import get_setter
from pyviews.rendering.expression import is_code_expression, parse_expression
from tkviews.node import WidgetNode

class StyleError(CoreError):
    '''Error for style'''
    NameMissing = 'Style name is missing'

class StyleItem:
    '''Wrapper under option'''
    def __init__(self, setter: Callable[[Node, str, Any]], name: str, value: Any):
        self._setter = setter
        self._name = name
        self._value = value

    def apply(self, node: Node):
        '''Applies option to passed node'''
        self._setter(node, self._name, self._value)

    def __hash__(self):
        return hash((self._name, self._setter))

    def __eq__(self, other: StyleItem):
        return hash(self) == hash(other)

class Style(Node):
    '''Node for storing config options'''
    def __init__(self, xml_node: XmlNode, node_globals: InheritedDict = None,
                 parent_name: str = None, styles: InheritedDict = None):
        super().__init__(xml_node, )
        self._parent_name = parent_name
        self._styles = styles
        self.name = None

    def set_items(self, items: List[StyleItem]):
        '''Sets style items'''
        if not self.name:
            raise StyleError(StyleError.NameMissing, self.xml_node.view_info)

        items = set(items)

        if self._parent_name:
            items.update(self._styles[self._parent_name])

        self._styles[self.name] = items

    def destroy(self):
        '''Removes self from styles'''
        self._styles.remove_key(self._name)
        self._destroy_bindings()

def set_style_items(node: Style):
    '''Parsing step. Parses attributes to style items and sets them to style'''
    attrs = node.xml_node.attrs
    try:
        node.name = next(attr.value for attr in attrs if attr.name == 'name')
    except StopIteration:
        raise StyleError(StyleError.NameMissing, node.xml_node.view_info)
    style_items = [_get_style_item(node, attr) for attr in attrs if attr.name != 'name']
    node.set_items(style_items)

def _get_style_item(node: Style, attr: XmlAttr):
    setter = get_setter(attr)
    value = attr.value
    if is_code_expression(value):
        expression = Expression(parse_expression(value)[1])
        value = expression.execute(node.globals.to_dictionary())
    return StyleItem(setter, attr.name, value)

def apply_styles(node: WidgetNode, style_keys: str):
    '''Applies styles to node'''
    keys = [key.strip() for key in style_keys.split(',')] \
            if isinstance(style_keys, str) else style_keys
    try:
        for key in [key for key in keys if key]:
            for item in node.styles[key]:
                item.apply(node)
    except KeyError as key_error:
        error = StyleError('Style is not found')
        error.add_info('Style name', key_error.args[0])
        raise error from key_error
