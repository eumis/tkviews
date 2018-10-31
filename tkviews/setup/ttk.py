from tkinter.ttk import Style
from pyviews import NodeSetup
from pyviews.core.compilation import Expression
from pyviews.rendering.expression import is_code_expression, parse_expression
from pyviews.rendering.flow import get_setter
from tkviews.core.ttk import TtkStyle

def get_ttk_style_setup() -> NodeSetup:
    '''Returns NodeSetup for TtkStyle'''
    setup = NodeSetup()
    setup.render_steps = [
        setup_value_setter,
        apply_style_attributes,
        configure
    ]

def setup_value_setter(node: TtkStyle, **args):
    '''Sets TtkStyle attribute setter'''
    node.setter = _value_setter

def _value_setter(node: TtkStyle, key: str, value):
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node.values[key] = value

def apply_style_attributes(node: TtkStyle, **args):
    '''Applies attributes'''
    for attr in node.xml_node.attrs:
        setter = get_setter(attr)
        value = attr.value if attr.value else ''
        if is_code_expression(value):
            expression = Expression(parse_expression(value)[1])
            value = expression.execute(node.globals.to_dictionary())
        setter(node, attr.name, value)

def configure(node: TtkStyle, **args):
    '''Sets style to widget'''
    ttk_style = Style()
    if not node.name:
        raise KeyError("style doesn't have name")
    ttk_style.configure(node.full_name, **node.values)
