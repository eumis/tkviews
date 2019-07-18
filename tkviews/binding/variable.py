"""Bindings specific for tkinter"""

from sys import exc_info
from typing import Type
from tkinter import Variable, Entry, Checkbutton, Radiobutton

from injectool import resolve
from pyviews.core import CoreError, XmlAttr, Node, Modifier
from pyviews.core import Binding, BindingTarget, BindingError, BindingRule
from pyviews.core import Expression
from pyviews.binding import PropertyTarget, get_expression_target, Binder
from pyviews.binding import ExpressionBinding, TwoWaysBinding
from pyviews.compilation import parse_expression


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
        except CoreError as error:
            self.add_error_info(error)
            raise
        except:
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

    def __init__(self, widget_type: Type, node_property: str, variable_property: str):
        self._widget_type = widget_type
        self._node_property = node_property
        self._variable_property = variable_property

    def suitable(self,
                 node: Node = None,
                 attr: XmlAttr = None,
                 **args) -> bool:
        try:
            return isinstance(node.instance, self._widget_type) and attr.name == self._node_property
        except AttributeError:
            return False

    def apply(self,
              node: Node = None,
              expr_body: str = None,
              modifier: Modifier = None,
              attr: XmlAttr = None,
              **args):
        (variable_type_key, expr_body) = parse_expression(expr_body)

        if variable_type_key in node.node_globals:
            self._set_variable(node, variable_type_key)
        variable = getattr(node, self._variable_property)

        expression_ = resolve(Expression, expr_body)
        expr_binding = self._create_expression_binding(node, expression_, attr, modifier)
        var_binding = self._create_variable_binding(node, expression_, variable)

        two_ways_binding = TwoWaysBinding(expr_binding, var_binding)
        two_ways_binding.bind()
        node.add_binding(two_ways_binding)

    def _set_variable(self, node: Node, variable_type_key: str):
        variable_type = node.node_globals[variable_type_key]
        variable = variable_type() if callable(variable_type) else variable_type
        node.set_attr(self._variable_property, variable)

    @staticmethod
    def _create_expression_binding(node: Node, expr: Expression, attr: XmlAttr, modifier: Modifier):
        target = PropertyTarget(node, attr.name, modifier)
        return ExpressionBinding(target, expr, node.node_globals)

    @staticmethod
    def _create_variable_binding(node: Node, expr: Expression, variable: Variable):
        target = get_expression_target(expr, node.node_globals)
        return VariableBinding(target, variable)


def add_variables_rules(binder: Binder):
    """Adds tkviews binding rules to passed factory"""
    binder.add_rule('twoways', VariableTwowaysRule(Entry, 'text', 'textvariable'))
    binder.add_rule('twoways', VariableTwowaysRule(Checkbutton, 'value', 'variable'))
    binder.add_rule('twoways', VariableTwowaysRule(Radiobutton, 'selected_value', 'variable'))
