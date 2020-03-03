"""Widgets binding"""

from tkinter import Widget, Variable, Entry, Checkbutton, Radiobutton, StringVar, BooleanVar, \
    IntVar
from typing import Type, Union

from pyviews.binding import BindingContext, TwoWaysBinding, ExpressionBinding, Binder, \
    get_expression_callback
from pyviews.core import BindingCallback, Binding, \
    BindingError, PyViewsError
from pyviews.core import error_handling
from pyviews.expression import Expression, execute


class VariableBinding(Binding):
    """Binding is subscribed on tkinter Var changes"""

    def __init__(self, callback: BindingCallback, var: Variable):
        super().__init__()
        self._callback = callback
        self._var = var
        self._trace_id = None

    def bind(self):
        """Applies binding"""
        self.destroy()
        self._trace_id = self._var.trace_add('write', self._var_callback)

    def _var_callback(self, *_):
        with error_handling(BindingError, self._add_error_info):
            value = self._var.get()
            self._callback(value)

    def _add_error_info(self, error: PyViewsError):
        error.add_info('Binding', self)
        error.add_info('Variable', self._var)
        error.add_info('Callback', self._callback)

    def destroy(self):
        """Destroys binding"""
        if self._trace_id:
            self._var.trace_remove('write', self._trace_id)
        self._trace_id = None


def add_variables_rules(binder: Binder):
    """Adds tkviews binding rules to passed factory"""
    binder.add_rule('twoways', lambda ctx: bind_variable_and_expression(StringVar, ctx),
                    lambda ctx: check_widget_and_property(Entry, 'textvariable', ctx))
    binder.add_rule('twoways', lambda ctx: bind_variable_and_expression(BooleanVar, ctx),
                    lambda ctx: check_widget_and_property(Checkbutton, 'variable', ctx))
    binder.add_rule('twoways', lambda ctx: bind_variable_and_expression(IntVar, ctx),
                    lambda ctx: check_widget_and_property(Radiobutton, 'variable', ctx))
    binder.add_rule('var', bind_custom_variable_and_expression)


def bind_variable_and_expression(variable: Union[Variable, Type[Variable]],
                                 context: BindingContext) -> TwoWaysBinding:
    """Create two ways binding between variable and expression"""
    if isinstance(variable, type):
        variable = variable()
    context.setter(context.node, context.xml_attr.name, variable)
    property_expression = Expression(context.expression_body)

    expr_binding = ExpressionBinding(variable.set, property_expression, context.node.node_globals)
    expression_callback = get_expression_callback(property_expression, context.node.node_globals)
    var_binding = VariableBinding(expression_callback, variable)
    two_ways_binding = TwoWaysBinding(expr_binding, var_binding)
    two_ways_binding.bind()
    return two_ways_binding


def check_widget_and_property(widget_type: Type[Widget], var_property: str,
                              context: BindingContext) -> bool:
    """Return true if type and property are matched with values from context"""
    try:
        return isinstance(context.node.instance, widget_type) \
               and context.xml_attr.name == var_property
    except AttributeError:
        return False


def bind_custom_variable_and_expression(context: BindingContext) -> TwoWaysBinding:
    """
    Create two ways binding between variable and expression.
    Expression should be "[binding type]:{[variable to bind]}:{[expression to bind]}"
    """
    (var_body, value_body) = context.expression_body.split('}:{')
    variable: Variable = execute(Expression(var_body), context.node.node_globals.to_dictionary())
    custom_context = BindingContext(context)
    custom_context.expression_body = value_body
    return bind_variable_and_expression(variable, custom_context)
