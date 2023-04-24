"""Common rendering functionality"""

from tkinter import Widget
from typing import Any, Tuple

from pyviews.core.expression import Expression, execute, is_expression, parse_expression
from pyviews.core.rendering import Node, NodeGlobals, RenderingContext, Setter, XmlNode
from pyviews.core.xml import XmlAttr
from pyviews.pipes import get_setter


class TkRenderingContext(RenderingContext):
    """tkviews rendering context"""

    @property
    def master(self) -> Widget:
        """master widget"""
        return self['master']

    @master.setter
    def master(self, value: Widget):
        self['master'] = value


def render_attribute(node: Node, xml_attr: XmlAttr) -> Tuple[Setter, Any]:
    """Returns setter and value"""
    setter = get_setter(xml_attr)
    value = xml_attr.value if xml_attr.value else ''
    if is_expression(value):
        expression_ = Expression(parse_expression(value)[1])
        value = execute(expression_, node.node_globals)
    return setter, value


def get_tk_child_context(child_xml_node: XmlNode, node: Node, context: TkRenderingContext) -> TkRenderingContext:
    """Return rendering context for child node"""
    return TkRenderingContext({
        'parent_node': node,
        'master': context.master,
        'node_globals': NodeGlobals(node.node_globals),
        'xml_node': child_xml_node
    })
