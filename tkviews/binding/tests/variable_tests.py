from unittest.mock import Mock, call

from pytest import mark
from pyviews.core import XmlAttr, Node
from tkviews.node import WidgetNode
from tkviews.binding.variable import VariableTarget, VariableBinding, VariableTwowaysRule


class TestVariable:
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


class Entry:
    pass


class Radiobutton:
    pass


class Checkbutton:
    pass


class VariableTwowaysRuleTests:
    @staticmethod
    @mark.parametrize('rule_args, suitable_args, expected', [
        ((Entry, 'text', 'textvariable'),
         {'node': WidgetNode(Entry(), Mock()), 'attr': XmlAttr('text')},
         True),
        ((Entry, 'text', 'textvariable'),
         {'node': WidgetNode(Radiobutton(), Mock()), 'attr': XmlAttr('text')},
         False),
        ((Radiobutton, 'selected_value', 'variable'),
         {'node': WidgetNode(Radiobutton(), Mock()), 'attr': XmlAttr('selected_value')},
         True),
        ((Radiobutton, 'selected_value', 'variable'),
         {'node': WidgetNode(Radiobutton(), Mock()), 'attr': XmlAttr('some_node_property')},
         False),
        ((Checkbutton, 'value', 'variable'),
         {'node': WidgetNode(Checkbutton(), Mock()), 'attr': XmlAttr('value')},
         True),
        ((Checkbutton, 'value', 'variable'),
         {'node': WidgetNode(Entry(), Mock()), 'attr': XmlAttr('some_node_property')},
         False)
    ])
    def test_suitable(rule_args: tuple, suitable_args: dict, expected: bool):
        """suitable() should check passed widget type and node property with passed arguments"""
        rule = VariableTwowaysRule(*rule_args)

        assert rule.suitable(**suitable_args) == expected

    @staticmethod
    @mark.parametrize('args', [
        {},
        {'node': WidgetNode(Entry(), Mock())},
        {'attr': XmlAttr('text')},
        {'node': Node(Mock()), 'attr': XmlAttr('text')},
        {'node': WidgetNode(Entry(), Mock()), 'attr': XmlAttr('some_property')}
    ])
    def test_suitable_checks_args(args: dict):
        """suitable() should return False for bad arguments"""
        rule = VariableTwowaysRule(Entry, 'text', 'textvariable')

        assert not rule.suitable(**args)
