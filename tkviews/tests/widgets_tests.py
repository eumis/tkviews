from tkinter import Variable, Widget
from unittest.mock import Mock, call

from pytest import mark, fixture
from pyviews.binding import BindingContext
from pyviews.core import XmlAttr, Node, ObservableEntity, Binding, InheritedDict
from pyviews.pipes import call_set_attr

from tkviews.widgets import VariableTarget, VariableBinding, WidgetNode, VariableTwowaysRule, bind, bind_all, config


class TestVariable(Variable):
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


@mark.parametrize('value', [1, 'value'])
def test_variable_target(value):
    """VariableTarget.on_change() should update variable value"""
    var = TestVariable()
    target = VariableTarget(var)

    target.on_change(value)

    assert var.get() == value


class VariableBindingTest:
    """VariableBinding class tests"""

    @staticmethod
    @mark.parametrize('value', [1, 'value'])
    def test_bind(value):
        """bind() should subscribe to var changes and propagate to target"""
        var = TestVariable()
        target = Mock()
        target.on_change = Mock()
        binding = VariableBinding(target, var)

        binding.bind()
        var.set(value)

        assert target.on_change.call_args == call(value)

    @staticmethod
    @mark.parametrize('value', [
        1, 'value', None,
        [1, 'str'],
    ])
    def test_destroy(value):
        """destroy() should remove subscription to var changes"""
        var = TestVariable()
        target = Mock()
        target.on_change = Mock()
        binding = VariableBinding(target, var)

        binding.bind()
        binding.destroy()
        var.set(value)

        assert not target.on_change.called


class Entry(Widget):
    # noinspection PyMissingConstructor
    def __init__(self):
        self.variable = None


class Radiobutton(Widget):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass


class Checkbutton(Widget):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass


class StringVar(Widget):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass


class IntVar(Widget):
    # noinspection PyMissingConstructor
    def __init__(self):
        pass


class TestViewModel(ObservableEntity):
    def __init__(self):
        super().__init__()
        self.value = None


@fixture
def apply_fixture(request):
    widget, var, vm = Entry(), TestVariable(), TestViewModel()
    node = WidgetNode(widget, Mock(), InheritedDict({'vm': vm}))

    context = BindingContext()
    context.node = node
    context.xml_attr = XmlAttr('variable')
    context.modifier = call_set_attr
    context.expression_body = "vm.value"

    request.cls.rule = VariableTwowaysRule(Entry, 'variable', TestVariable)
    request.cls.context = context
    request.cls.widget = widget
    request.cls.vm = vm


@mark.usefixtures('apply_fixture')
class VariableTwowaysRuleTests:
    @staticmethod
    @mark.parametrize('rule_args, binding_context, expected', [
        ((Entry, 'textvariable', StringVar),
         {'node': WidgetNode(Entry(), Mock()), 'xml_attr': XmlAttr('textvariable')},
         True),
        ((Entry, 'textvariable', StringVar),
         {'node': WidgetNode(Radiobutton(), Mock()), 'xml_attr': XmlAttr('textvariable')},
         False),
        ((Radiobutton, 'variable', IntVar),
         {'node': WidgetNode(Radiobutton(), Mock()), 'xml_attr': XmlAttr('variable')},
         True),
        ((Radiobutton, 'variable', IntVar),
         {'node': WidgetNode(Radiobutton(), Mock()), 'xml_attr': XmlAttr('some_node_property')},
         False)
    ])
    def test_suitable(rule_args: tuple, binding_context: dict, expected: bool):
        """suitable() should check passed widget type and node property with passed arguments"""
        rule = VariableTwowaysRule(*rule_args)

        assert rule.suitable(BindingContext(**binding_context)) == expected

    @staticmethod
    @mark.parametrize('args', [
        {},
        {'node': WidgetNode(Entry(), Mock())},
        {'xml_attr': XmlAttr('text')},
        {'node': Node(Mock()), 'xml_attr': XmlAttr('text')},
        {'node': WidgetNode(Entry(), Mock()), 'xml_attr': XmlAttr('some_property')}
    ])
    def test_suitable_checks_args(args: dict):
        """suitable() should return False for bad arguments"""
        rule = VariableTwowaysRule(Entry, 'text', TestVariable)

        assert not rule.suitable(BindingContext(args))

    def test_apply_return_binding(self):
        """should return binding"""
        binding = self.rule.apply(self.context)

        assert isinstance(binding, Binding)

    def test_apply_create_variable(self):
        """should create variable with set up variable type"""
        self.rule.apply(self.context)

        assert isinstance(self.widget.variable, TestVariable)

    @mark.parametrize('init_value, new_value', [
        (1, 2),
        (2, 2),
        ('one', 'two')
    ])
    def test_apply_binds_variable_to_expression(self, init_value, new_value):
        """should bind variable to expression"""
        self.vm.value = init_value

        self.rule.apply(self.context)
        self.vm.value = new_value

        assert self.widget.variable.get() == new_value

    @mark.parametrize('init_value, new_value', [
        (1, 2),
        (2, 2),
        ('one', 'two')
    ])
    def test_apply_binds_expression_to_variable(self, init_value, new_value):
        """should bind variable to expression"""
        self.vm.value = init_value

        self.rule.apply(self.context)
        self.widget.variable.set(new_value)

        assert self.vm.value == new_value


def test_bind():
    """bind() should call bind for instance"""
    node = Mock()

    bind(node, 'event', lambda: None)

    assert node.bind.called


def test_bind_all():
    """bind_all() should call bind_all of instance"""
    node = Mock()

    bind_all(node, 'event', lambda: None)

    assert node.bind_all.called


@mark.parametrize('key, value', [
    ('key', 1),
    ('other_key', 'value')
])
def test_config(key, value):
    """config() should call config of widget from WidgetNode with passed parameters"""
    node = Mock(instance=Mock())

    config(node, key, value)

    assert node.instance.config.call_args == call(**{key: value})
