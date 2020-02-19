"""ttk specific implementation"""
from functools import partial
from tkinter.ttk import Style, Widget
from typing import Any

from pyviews.core import XmlNode, Node, InstanceNode, InheritedDict
from pyviews.rendering import RenderingPipeline, get_type, create_instance

from tkviews.core import TkNode
from tkviews.core.rendering import TkRenderingContext, render_attribute


class TtkWidgetNode(InstanceNode, TkNode):
    """Wrapper under ttk widget"""

    def __init__(self, widget: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(widget, xml_node, node_globals=node_globals)
        self._node_styles = node_styles

    @property
    def node_styles(self) -> InheritedDict:
        """Returns node styles set"""
        return self._node_styles

    @property
    def ttkstyle(self):
        """Returns ttk style"""
        return self.instance.cget('style')

    @ttkstyle.setter
    def ttkstyle(self, value):
        self.instance.config(style=value)


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


def get_ttk_style_setup() -> RenderingPipeline:
    """Returns RenderingPipeline for TtkStyle"""
    return RenderingPipeline([
        setup_value_setter,
        apply_style_attributes,
        configure
    ], create_node=_create_ttk_widget_node)


def _create_ttk_widget_node(context: TkRenderingContext):
    inst_type = get_type(context.xml_node)
    inst = create_instance(inst_type, context)
    return create_instance(TtkWidgetNode, {'widget': inst, **context})


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
    ttk_style = Style()
    if not node.name:
        raise KeyError("style doesn't have name")
    ttk_style.configure(node.full_name, **node.values)
