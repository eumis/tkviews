'''Bindings specific for tkinter'''

from sys import exc_info
from tkinter import Variable, StringVar, Entry, Checkbutton
from pyviews.core import CoreError
from pyviews.core.compilation import Expression
from pyviews.core.binding import Binding, BindingTarget, BindingError
from pyviews.core.binding import InstanceTarget, get_expression_target
from pyviews.core.binding import ExpressionBinding, TwoWaysBinding
from pyviews.rendering.binding import BindingFactory, BindingArgs
from pyviews.rendering.expression import parse_expression

class VariableTarget(BindingTarget):
    '''Target is tkinter Var'''
    def __init__(self, var: Variable):
        self._var = var

    def on_change(self, value):
        self._var.set(value)

class VariableBinding(Binding):
    '''Binding is subscribed on tkinter Var changes'''
    def __init__(self, target: BindingTarget, var: Variable):
        self._target = target
        self._var = var
        self._trace_id = None

    def bind(self):
        self.destroy()
        self._trace_id = self._var.trace_add('write', self._callback)

    def _callback(self, *args):
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

def add_rules(factory: BindingFactory):
    '''Adds tkviews binding rules to passed factory'''
    factory.add_rule('twoways', BindingFactory.Rule(is_entry_twoways, apply_entry_twoways))
    factory.add_rule('twoways', BindingFactory.Rule(is_check_twoways, apply_checkbutton_twoways))

def is_entry_twoways(args: BindingArgs):
    '''suitable for Entry two ways binding'''
    try:
        return isinstance(args.node.widget, Entry)
    except AttributeError:
        return False

def apply_entry_twoways(args: BindingArgs):
    '''
    Applies "twoways" binding.
    Expression result is assigned to property.
    Property is set on expression change.
    Wrapped instance is changed on property change
    '''
    (var_key, expr_body) = parse_expression(args.expr_body)
    var = args.node.globals[var_key]() \
                if args.node.globals.has_key(var_key) else StringVar()
    args.node.widget.config(textvariable=var)
    args.node.define_setter('text', lambda node, value: var.set(value))

    expression = Expression(expr_body)
    target = InstanceTarget(args.node, args.attr.name, args.modifier)
    expr_binding = ExpressionBinding(target, expression, args.node.globals)

    target = get_expression_target(expression, args.node.globals)
    obs_binding = VariableBinding(target, var)

    two_ways_binding = TwoWaysBinding(expr_binding, obs_binding)
    two_ways_binding.bind()
    args.node.add_binding(two_ways_binding)

def is_check_twoways(args: BindingArgs):
    '''suitable for Checkbutton two ways binding'''
    try:
        return isinstance(args.node.widget, Checkbutton)
    except AttributeError:
        return False

def apply_checkbutton_twoways(args: BindingArgs):
    '''Applies twoways binding for Checkbutton. BooleanVar is used by default'''
    (var_key, expr_body) = parse_expression(args.expr_body)
    if args.node.globals.has_key(var_key):
        args.node.variable = args.node.globals[var_key]()

    expression = Expression(expr_body)
    target = InstanceTarget(args.node, args.attr.name, args.modifier)
    expr_binding = ExpressionBinding(target, expression, args.node.globals)

    target = get_expression_target(expression, args.node.globals)
    obs_binding = VariableBinding(target, args.node.variable)

    two_ways_binding = TwoWaysBinding(expr_binding, obs_binding)
    two_ways_binding.bind()
    args.node.add_binding(two_ways_binding)