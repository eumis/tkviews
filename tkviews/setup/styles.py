
from pyviews import NodeSetup
from pyviews.core import CoreError
from pyviews.core.xml import XmlAttr
from pyviews.core.compilation import Expression
from pyviews.core.observable import InheritedDict
from pyviews.rendering.flow import get_setter
from pyviews.rendering.expression import is_code_expression, parse_expression
from tkviews.core.widgets import WidgetNode
from tkviews.core.styles import Style, StyleItem

class StyleError(CoreError):
    '''Error for style'''
    NameMissing = 'Style name is missing'

def get_style_setup() -> NodeSetup:
    '''Returns setup for style node'''
    node_setup = NodeSetup()
    node_setup.render_steps = [
        apply_style_items,
        apply_parent_items,
        store_to_node_styles
    ]
    return node_setup

def apply_style_items(node: Style, **args):
    '''Parsing step. Parses attributes to style items and sets them to style'''
    attrs = node.xml_node.attrs
    try:
        node.name = next(attr.value for attr in attrs if attr.name == 'name')
    except StopIteration:
        raise StyleError(StyleError.NameMissing, node.xml_node.view_info)
    node.items = {attr.name: _get_style_item(node, attr) for attr in attrs if attr.name != 'name'}

def _get_style_item(node: Style, attr: XmlAttr):
    setter = get_setter(attr)
    value = attr.value.strip() if attr.value else ''
    if is_code_expression(value):
        expression = Expression(parse_expression(value)[1])
        value = expression.execute(node.globals.to_dictionary())
    return StyleItem(setter, attr.name, value)

def apply_parent_items(node: Style, parent_name: str = None, node_styles: InheritedDict = None, **args):
    '''Sets style items from parent style'''
    if parent_name:
        parent_items = node_styles[parent_name]
        node.items = {**parent_items, **node.items}

def store_to_node_styles(node: Style, node_styles: InheritedDict = None, **args):
    '''Store styles to node styles'''
    node_styles[node.name] = node.items

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
