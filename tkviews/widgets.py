"""Tkinter widgets nodes"""
from sys import exc_info
from tkinter import Tk, Widget, Variable, Entry, Checkbutton, Radiobutton, StringVar, BooleanVar, IntVar
from typing import Type

from pyviews.binding import BindingRule, BindingContext, TwoWaysBinding, ExpressionBinding, \
    get_expression_target, Binder
from pyviews.compilation import parse_expression, Expression
from pyviews.core import XmlNode, InstanceNode, InheritedDict, XmlAttr, BindingTarget, Binding, ViewsError, \
    BindingError, Node
from pyviews.pipes import apply_attributes, render_children, apply_attribute
from pyviews.rendering import RenderingPipeline, get_type, create_instance

from tkviews.core import TkNode
from tkviews.core.common import TkRenderingContext
from tkviews.styles import StyleError


class Root(InstanceNode, TkNode):
    """Wrapper under tkinter Root"""

    def __init__(self, xml_node: XmlNode):
        super().__init__(Tk(), xml_node)
        self._icon = None
        self._node_styles = InheritedDict()

    @property
    def node_styles(self) -> InheritedDict:
        """Returns node styles set"""
        return self._node_styles

    @property
    def state(self):
        """Widget state"""
        return self.instance.state()

    @state.setter
    def state(self, state):
        self.instance.state(state)

    @property
    def icon(self):
        """Icon path"""
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.instance.iconbitmap(default=value)

    def bind(self, event, command):
        """Calls widget bind"""
        self.instance.bind(event, command)

    def bind_all(self, event, command):
        """Calls widget bind"""
        self.instance.bind_all(event, command)


def get_root_setup() -> RenderingPipeline:
    """Returns setup for root"""
    return RenderingPipeline(pipes=[
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        render_widget_children
    ])


class WidgetNode(InstanceNode, TkNode):
    """Wrapper under tkinter widget"""

    def __init__(self, widget: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(widget, xml_node, node_globals=node_globals)
        self._node_styles = InheritedDict(node_styles)

    @property
    def node_styles(self) -> InheritedDict:
        """Returns node styles set"""
        return self._node_styles

    def bind(self, event, command):
        """Calls widget bind"""
        self.instance.bind(event, command)

    def bind_all(self, event, command):
        """Calls widget bind"""
        self.instance.bind_all(event, command)


def get_widget_setup():
    """Returns setup for widget"""
    return RenderingPipeline([
        setup_properties,
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        apply_text,
        render_widget_children
    ], create_node=_create_widget_node)


def setup_widget_setter(node: WidgetNode, _: TkRenderingContext):
    """Sets up setter"""
    node.attr_setter = _widget_node_setter


def _widget_node_setter(node: WidgetNode, key: str, value):
    """Applies passed attribute"""
    if hasattr(node, key):
        setattr(node, key, value)
    elif hasattr(node.instance, key):
        setattr(node.instance, key, value)
    else:
        node.instance.configure(**{key: value})


def setup_widget_destroy(node: WidgetNode, _: TkRenderingContext):
    """Sets up on destroy method"""
    node.on_destroy = _on_widget_destroy


def _on_widget_destroy(node: WidgetNode):
    node.instance.destroy()


def render_widget_children(node: WidgetNode, context: TkRenderingContext):
    render_children(node, context, _get_child_context)


def _get_child_context(xml_node: XmlNode, node: WidgetNode, _: TkRenderingContext):
    """Renders child widgets"""
    child_context = TkRenderingContext()
    child_context.xml_node = xml_node
    child_context.parent_node = node
    child_context.master = node.instance
    child_context.node_globals = InheritedDict(node.node_globals)
    child_context.node_styles = InheritedDict(node.node_styles)
    return child_context


def _create_widget_node(context: TkRenderingContext):
    inst_type = get_type(context.xml_node)
    inst = create_instance(inst_type, context)
    return create_instance(WidgetNode, {'widget': inst, **context})


def setup_properties(node: WidgetNode, _: TkRenderingContext):
    """Sets up widget node properties"""
    # node.properties['geometry'] = Property('geometry', _geometry_setter, node=node)
    # node.properties['style'] = Property('style', _style_setter, node=node)


# def _geometry_setter(node: WidgetNode, geometry: Geometry, previous: Geometry):
#     if previous:
#         previous.forget(node.instance)
#     if geometry is not None:
#         geometry.apply(node.instance)
#     return geometry
#
#
# def _style_setter(node: WidgetNode, styles: str):
#     apply_styles(node, styles)
#     return styles


def apply_styles(node: WidgetNode, style_keys: str):
    """Applies styles to node"""
    keys = [key.strip() for key in style_keys.split(',')] \
        if isinstance(style_keys, str) else style_keys
    try:
        for key in [key for key in keys if key]:
            for item in node.node_styles[key]:
                item.apply(node)
    except KeyError as key_error:
        error = StyleError('Style is not found')
        error.add_info('Style name', key_error.args[0])
        raise error from key_error


def apply_text(node: WidgetNode, _: TkRenderingContext):
    """Applies xml node content to WidgetNode"""
    if node.xml_node.text is None or not node.xml_node.text.strip():
        return
    text_attr = XmlAttr('text', node.xml_node.text)
    apply_attribute(node, text_attr)


class VariableTarget(BindingTarget):
    """Target is tkinter Var"""

    def __init__(self, var: Variable):
        self._var = var

    def on_change(self, value):
        self._var.set(value)


class VariableBinding(Binding):
    """Binding is subscribed on tkinter Var changes"""

    def __init__(self, target: BindingTarget, var: Variable):
        super().__init__()
        self._target = target
        self._var = var
        self._trace_id = None

    def bind(self):
        self.destroy()
        self._trace_id = self._var.trace_add('write', self._callback)

    def _callback(self, *_):
        try:
            value = self._var.get()
            self._target.on_change(value)
        except ViewsError as error:
            self.add_error_info(error)
            raise
        except BaseException:
            info = exc_info()
            error = BindingError(BindingError.TargetUpdateError)
            self.add_error_info(error)
            raise error from info[1]

    def destroy(self):
        if self._trace_id:
            self._var.trace_remove('write', self._trace_id)
        self._trace_id = None


class VariableTwowaysRule(BindingRule):
    """Rule for two ways binding between property and expression using variable"""

    def __init__(self, widget_type: Type, variable_property: str, variable_type: Type):
        self._widget_type = widget_type
        self._variable_property = variable_property
        self._variable_type = variable_type

    def suitable(self, context: BindingContext) -> bool:
        try:
            return isinstance(context.node.instance, self._widget_type) \
                   and context.xml_attr.name == self._variable_property
        except AttributeError:
            return False

    def apply(self, context: BindingContext):
        (variable_type_key, expr_body) = parse_expression(context.expression_body)
        variable: Variable = self._variable_type()
        context.modifier(context.node, context.xml_attr.name, variable)

        expression_ = Expression(expr_body)
        expr_binding = self._bind_variable_to_expression(context.node, expression_, variable)
        var_binding = self._bind_vm_to_variable(context.node, expression_, variable)

        two_ways_binding = TwoWaysBinding(expr_binding, var_binding)
        two_ways_binding.bind()
        return two_ways_binding

    @staticmethod
    def _bind_variable_to_expression(node: Node, expr: Expression, variable: Variable):
        target = VariableTarget(variable)
        return ExpressionBinding(target, expr, node.node_globals)

    @staticmethod
    def _bind_vm_to_variable(node: Node, expr: Expression, variable: Variable):
        target = get_expression_target(expr, node.node_globals)
        return VariableBinding(target, variable)


def add_variables_rules(binder: Binder):
    """Adds tkviews binding rules to passed factory"""
    binder.add_rule('twoways', VariableTwowaysRule(Entry, 'textvariable', StringVar))
    binder.add_rule('twoways', VariableTwowaysRule(Checkbutton, 'variable', BooleanVar))
    binder.add_rule('twoways', VariableTwowaysRule(Radiobutton, 'variable', IntVar))
