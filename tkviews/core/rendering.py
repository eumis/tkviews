"""Common rendering functionality"""

from tkinter import Widget
from typing import Tuple, Any

from pyviews.core import InheritedDict, Node, XmlAttr, Setter
from pyviews.expression import is_expression, parse_expression, Expression, execute
from pyviews.pipes import get_setter
from pyviews.rendering import RenderingContext


class TkRenderingContext(RenderingContext):
    """tkviews rendering context"""

    @property
    def master(self) -> Widget:
        """master widget"""
        return self['master']

    @master.setter
    def master(self, value: Widget):
        self['master'] = value

    @property
    def node_styles(self) -> InheritedDict:
        """node styles"""
        return self['node_styles']

    @node_styles.setter
    def node_styles(self, value: InheritedDict):
        self['node_styles'] = value


def render_attribute(node: Node, xml_attr: XmlAttr) -> Tuple[Setter, Any]:
    """Returns setter and value"""
    setter = get_setter(xml_attr)
    value = xml_attr.value if xml_attr.value else ''
    if is_expression(value):
        expression_ = Expression(parse_expression(value)[1])
        value = execute(expression_, node.node_globals.to_dictionary())
    return setter, value
