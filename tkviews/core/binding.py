'''Bindings specific for tkinter'''

from sys import exc_info
from tkinter import Variable, Entry, Checkbutton, Radiobutton
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

# TODO updates binding rules and write tests
def add_rules(factory: BindingFactory):
    '''Adds tkviews binding rules to passed factory'''
    factory.add_rule('twoways', _get_rule(Entry, 'text', apply_entry_twoways))
    factory.add_rule('twoways', _get_rule(Checkbutton, 'value', apply_var_two_ways))
    factory.add_rule('twoways', _get_rule(Radiobutton, 'selected_value', apply_var_two_ways))

def _get_rule(target_type, attr, apply):
    return BindingFactory.Rule(
        lambda args: _is_suitable(args, target_type, attr),
        apply)

def _is_suitable(args: BindingArgs, target_type, attr):
    try:
        return isinstance(args.node.instance, target_type) and args.attr.name == attr
    except AttributeError:
        return False

def apply_entry_twoways(args: BindingArgs):
    '''Applies twoways binding for entry text'''
    apply_var_two_ways(args, 'textvariable')

def apply_var_two_ways(args: BindingArgs, var_property=None):
    '''Applies twoways binding using tkinter variable.'''
    var_property = var_property if var_property else 'variable'
    (var_key, expr_body) = parse_expression(args.expr_body)
    if args.node.node_globals.has_key(var_key):
        val = args.node.node_globals[var_key]
        var = val() if callable(val) else val
        args.node.set_attr(var_property, var)

    _apply_two_ways(args, expr_body, getattr(args.node, var_property))

def _apply_two_ways(args: BindingArgs, expr_body: str, var: Variable):
    '''Applies two ways binding between tkinter Variable and expression'''
    expression = Expression(expr_body)
    target = InstanceTarget(args.node, args.attr.name, args.modifier)
    expr_binding = ExpressionBinding(target, expression, args.node.node_globals)

    target = get_expression_target(expression, args.node.node_globals)
    obs_binding = VariableBinding(target, var)

    two_ways_binding = TwoWaysBinding(expr_binding, obs_binding)
    two_ways_binding.bind()
    args.node.add_binding(two_ways_binding)
