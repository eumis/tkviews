'''Nodes for storing config options for widgets'''

from pyviews.core.xml import XmlAttr
from pyviews.core.ioc import inject
from pyviews.core.compilation import Expression
from pyviews.core.node import Node
from pyviews.rendering.expression import is_code_expression, parse_expression
from pyviews.rendering.core import get_modifier

class StyleItem:
    '''Wrapper under option'''
    def __init__(self, modifier, name, value):
        self._modifier = modifier
        self._name = name
        self._value = value

    def apply(self, node: Node):
        '''Applies option to passed node'''
        self._modifier(node, self._name, self._value)

class Style(Node):
    '''Node for storing config options'''
    def __init__(self, xml_node, parent_context=None, parent_style: str = None):
        super().__init__(xml_node, parent_context)
        self._parent_style = parent_style
        self.name = None

    @inject('styles')
    def set_items(self, items, styles: dict = None):
        '''Sets style items'''
        if not self.name:
            raise KeyError("style doesn't have name")
        if self._parent_style:
            parent_items = [pi for pi in styles[self._parent_style] \
                if self._not_it_items(pi, items)]
            items = parent_items + items
        styles[self.name] = items

    def _not_it_items(self, item, items):
        return all(i._name != item._name or i._modifier != item._modifier \
                   for i in items)

    def get_node_args(self, xml_node):
        args = super().get_node_args(xml_node)
        args['parent_style'] = self.name
        return args

    @inject('styles')
    def destroy(self, styles=None):
        '''Removes self from styles'''
        del styles[self.name]
        self._destroy_bindings()

def apply_attributes(node: Style):
    '''Parsing step. Parses attributes to style items and sets them to style'''
    attrs = node.xml_node.attrs
    try:
        node.name = next(attr.value for attr in attrs if attr.name == 'name')
    except StopIteration:
        raise KeyError('name attribute is required for style')
    style_items = [_get_item(node, attr) for attr in attrs if attr.name != 'name']
    node.set_items(style_items)

def _get_item(node: Style, attr: XmlAttr):
    modifier = get_modifier(attr)
    value = attr.value
    if is_code_expression(value):
        expression = Expression(parse_expression(value)[1])
        value = expression.execute(node.globals.to_dictionary())
    return StyleItem(modifier, attr.name, value)

@inject('styles')
def apply_styles(node: Node, style_keys, styles: dict = None):
    '''Applies passed styles to node'''
    keys = [key.strip() for key in style_keys.split(',')] \
            if isinstance(style_keys, str) else style_keys
    for key in [key for key in keys if key]:
        for item in styles[key]:
            item.apply(node)
