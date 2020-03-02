from tkinter import Widget
from typing import Type
from unittest.mock import Mock, call

from pytest import mark, fixture
from pyviews.binding import BindingContext, TwoWaysBinding
from pyviews.core import XmlAttr, Node, ObservableEntity, InheritedDict
from pyviews.pipes import call_set_attr

from tkviews.widgets.binding import VariableBinding, check_widget_and_property, \
    bind_variable_and_expression, bind_custom_variable_and_expression
from tkviews.widgets.node import WidgetNode


class TestVariable:
    # noinspection PyMissingConstructor
    def __init__(self):
        self._val = None
        self._callback = None

    def set(self, value):
        self._val = value
        if self._callback:
            self._callback()

    def get(self):
        return self._val

    def trace_add(self, mode, callback):
        if mode == 'write':
            self._callback = callback
        return 'trace id'

    def trace_remove(self, mode, trace_id):
        if mode == 'write' and trace_id == 'trace id':
            self._callback = None


class VariableBindingTest:
    """VariableBinding tests"""

    @staticmethod
    @mark.parametrize('value', [1, 'value'])
    def test_bind(value):
        """bind() should subscribe to var changes and propagate to target"""
        var = TestVariable()
        callback = Mock()
        binding = VariableBinding(callback, var)

        binding.bind()
        var.set(value)

        assert callback.call_args == call(value)

    @staticmethod
    @mark.parametrize('value', [
        1, 'value', None,
        [1, 'str'],
    ])
    def test_destroy(value):
        """destroy() should remove subscription to var changes"""
        var = TestVariable()
        callback = Mock()
        binding = VariableBinding(callback, var)

        binding.bind()
        binding.destroy()
        var.set(value)

        assert not callback.called


class Entry(Widget):
    # noinspection PyMissingConstructor
    def __init__(self):
        self.variable = None


class Radiobutton(Widget):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass


class TestViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.value = None


@fixture
def var_binding_fixture(request):
    widget, vm = Entry(), TestViewModel()
    node = WidgetNode(widget, Mock(), InheritedDict({'vm': vm}))

    context = BindingContext()
    context.node = node
    context.xml_attr = XmlAttr('variable')
    context.setter = call_set_attr
    context.expression_body = "vm.value"

    request.cls.context = context
    request.cls.widget = widget
    request.cls.vm = vm


@mark.usefixtures('var_binding_fixture')
class BindVariableAndExpressionTests:
    """bind_variable_and_expression() tests"""

    def test_returns_binding(self):
        """should return binding"""
        binding = bind_variable_and_expression(TestVariable, self.context)

        assert isinstance(binding, TwoWaysBinding)

    def test_sets_variable_of_passed_type(self):
        """should create variable of passed type and set it using setter from context"""
        bind_variable_and_expression(TestVariable, self.context)

        assert isinstance(self.widget.variable, TestVariable)

    def test_sets_variable(self):
        """should set passed variable using setter from context"""
        var = TestVariable()

        bind_variable_and_expression(var, self.context)

        assert self.widget.variable is var

    @mark.parametrize('init_value, new_value', [
        (1, 2),
        (2, 2),
        ('one', 'two')
    ])
    def test_binds_variable_to_expression(self, init_value, new_value):
        """should bind variable to expression"""
        self.vm.value = init_value

        bind_variable_and_expression(TestVariable, self.context)
        self.vm.value = new_value

        assert self.widget.variable.get() == new_value

    @mark.parametrize('init_value, new_value', [
        (1, 2),
        (2, 2),
        ('one', 'two')
    ])
    def test_binds_expression_to_variable(self, init_value, new_value):
        """should bind expression to variable"""
        self.vm.value = init_value

        bind_variable_and_expression(TestVariable, self.context)
        self.widget.variable.set(new_value)

        assert self.vm.value == new_value


class CheckWidgetAndPropertyTests:
    """check_widget_and_property() tests"""

    @staticmethod
    @mark.parametrize('widget_type, var_property, binding_context, expected', [
        (Entry, 'textvariable',
         {'node': WidgetNode(Entry(), Mock()), 'xml_attr': XmlAttr('textvariable')},
         True),
        (Entry, 'textvariable',
         {'node': WidgetNode(Radiobutton(), Mock()), 'xml_attr': XmlAttr('textvariable')},
         False),
        (Radiobutton, 'variable',
         {'node': WidgetNode(Radiobutton(), Mock()), 'xml_attr': XmlAttr('variable')},
         True),
        (Radiobutton, 'variable',
         {'node': WidgetNode(Radiobutton(), Mock()), 'xml_attr': XmlAttr('some_node_property')},
         False)
    ])
    def test_checks_type_and_property(widget_type: Type[Widget], var_property: str,
                                      binding_context: dict, expected: bool):
        """should return true if widget type and var property equal to items from context"""
        actual = check_widget_and_property(widget_type, var_property,
                                           BindingContext(**binding_context))

        assert actual == expected

    @staticmethod
    @mark.parametrize('context', [
        {},
        {'node': WidgetNode(Entry(), Mock())},
        {'xml_attr': XmlAttr('text')},
        {'node': Node(Mock()), 'xml_attr': XmlAttr('text')},
        {'node': WidgetNode(Entry(), Mock()), 'xml_attr': XmlAttr('some_property')}
    ])
    def test_returns_false_for_bad_context(context: dict):
        """should return false if context is incomplete"""
        assert not check_widget_and_property(Entry, 'textvariable',
                                             BindingContext(context))


@fixture
# pylint: disable=redefined-outer-name,unused-argument
def custom_var_binding_fixture(var_binding_fixture, request):
    var = TestVariable()
    request.cls.variable = var
    request.cls.context.node.node_globals['variable'] = var
    request.cls.context.expression_body = "variable}:{vm.value"


@mark.usefixtures('custom_var_binding_fixture')
class BindCustomVariableAndExpressionTests:
    """bind_custom_variable_and_expression() tests"""

    def test_returns_binding(self):
        """should return binding"""
        binding = bind_custom_variable_and_expression(self.context)

        assert isinstance(binding, TwoWaysBinding)

    def test_sets_variable_of_passed_type(self):
        """should use variable from first part of expression"""
        bind_custom_variable_and_expression(self.context)

        assert self.widget.variable is self.variable

    @mark.parametrize('init_value, new_value', [
        (1, 2),
        (2, 2),
        ('one', 'two')
    ])
    def test_binds_variable_to_expression(self, init_value, new_value):
        """should bind variable to second part of expression"""
        self.vm.value = init_value

        bind_custom_variable_and_expression(self.context)
        self.vm.value = new_value

        assert self.variable.get() == new_value

    @mark.parametrize('init_value, new_value', [
        (1, 2),
        (2, 2),
        ('one', 'two')
    ])
    def test_binds_expression_to_variable(self, init_value, new_value):
        """should bind second part of expression to variable"""
        self.vm.value = init_value

        bind_custom_variable_and_expression(self.context)
        self.variable.set(new_value)

        assert self.vm.value == new_value
