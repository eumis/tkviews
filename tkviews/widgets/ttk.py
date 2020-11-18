"""ttk specific implementation"""
from functools import partial
from tkinter.ttk import Style
from typing import Any

from pyviews.core import XmlNode, Node, InheritedDict
from pyviews.rendering import RenderingPipeline

from tkviews.core.rendering import TkRenderingContext, render_attribute


class TtkStyle(Node):
    """Node for tkk style"""

    def __init__(self, xml_node: XmlNode, parent_name=None, node_globals: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self.values = {}
        self._parent_name = parent_name
        self.name = None

    @property
    def full_name(self):
        """Full name"""
        return '{0}.{1}'.format(self.name, self._parent_name) \
            if self._parent_name else self.name


def theme_use(_node: Node, key: str, _value: Any):
    """Sets ttk style theme"""
    ttk_style = Style()
    ttk_style.theme_use(key)


def get_ttk_style_pipeline() -> RenderingPipeline:
    """Returns RenderingPipeline for TtkStyle"""
    return RenderingPipeline([
        setup_value_setter,
        apply_style_attributes,
        configure
    ], name='ttk style pipeline')


def setup_value_setter(node: TtkStyle, _: TkRenderingContext):
    """Sets TtkStyle attribute setter"""
    node.set_attr = partial(_value_setter, node)


def _value_setter(node: TtkStyle, key: str, value):
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node.values[key] = value


def apply_style_attributes(node: TtkStyle, _: TkRenderingContext):
    """Applies attributes"""
    for xml_attr in node.xml_node.attrs:
        setter, value = render_attribute(node, xml_attr)
        setter(node, xml_attr.name, value)


def configure(node: TtkStyle, _: TkRenderingContext):
    """Sets style to widget"""
    if not node.name:
        raise KeyError("style doesn't have name")
    Style().configure(node.full_name, **node.values)
