#pylint: disable=missing-docstring,invalid-name

from unittest import TestCase
from unittest.mock import Mock, call
from tkinter import Variable, Tk
from pyviews.testing import case
from pyviews.core import XmlAttr, Node
from tkviews.node import WidgetNode
from .variable import VariableTarget, VariableBinding, VariableTwowaysRule

class TestVariableTarget(TestCase):
    def setUp(self):
        self.root = Tk()

    @case(1)
    @case('value')
    def test_on_change_set_var(self, value):
        var = Variable()
        target = VariableTarget(var)

        target.on_change(value)

        msg = 'on_change set value to variable'
        self.assertEqual(var.get(), value, msg)

    def tearDown(self):
        self.root.destroy()

class TestVariableBinding(TestCase):
    def setUp(self):
        self.root = Tk()

    @case(1)
    @case('value')
    def test_bind_should_subscribe_to_var_changes(self, value):
        var = Variable()
        target = Mock()
        target.on_change = Mock()
        binding = VariableBinding(target, var)

        binding.bind()
        var.set(value)

        msg = 'bind should subscribe to var changes and propagate to target'
        self.assertEqual(target.on_change.call_args, call(value), msg)

    @case(1)
    @case('value')
    @case(None)
    @case([1, 'str'])
    def test_destroy_removes_binding(self, value):
        var = Variable()
        target = Mock()
        target.on_change = Mock()
        binding = VariableBinding(target, var)

        binding.bind()
        binding.destroy()
        var.set(value)

        msg = 'destroy should remove subscribtion to var changes'
        self.assertFalse(target.on_change.called, msg)

    def test_destroy_does_nothing_if_bind_not_called(self):
        var = Variable()
        target = Mock()
        binding = VariableBinding(target, var)

        binding.destroy()

    def tearDown(self):
        self.root.destroy()

class Entry:
    pass

class Radiobutton:
    pass

class Checkbutton:
    pass

class VariableTwowaysRule_suitable_tests(TestCase):
    @case(VariableTwowaysRule(Entry, 'text', 'textvariable'),
          {'node': WidgetNode(Entry(), Mock()), 'attr': XmlAttr('text')},
          True)
    @case(VariableTwowaysRule(Entry, 'text', 'textvariable'),
          {'node': WidgetNode(Radiobutton(), Mock()), 'attr': XmlAttr('text')},
          False)
    @case(VariableTwowaysRule(Radiobutton, 'selected_value', 'variable'),
          {'node': WidgetNode(Radiobutton(), Mock()), 'attr': XmlAttr('selected_value')},
          True)
    @case(VariableTwowaysRule(Radiobutton, 'selected_value', 'variable'),
          {'node': WidgetNode(Radiobutton(), Mock()), 'attr': XmlAttr('some_node_property')},
          False)
    @case(VariableTwowaysRule(Checkbutton, 'value', 'variable'),
          {'node': WidgetNode(Checkbutton(), Mock()), 'attr': XmlAttr('value')},
          True)
    @case(VariableTwowaysRule(Checkbutton, 'value', 'variable'),
          {'node': WidgetNode(Entry(), Mock()), 'attr': XmlAttr('some_node_property')},
          False)
    def test_checks_widget_type_and_property(self, rule: VariableTwowaysRule, args: dict, expected: bool):
        actual = rule.suitable(**args)

        msg = 'should check passed widget type and node property with passed arguments'
        self.assertEqual(expected, actual, msg)

    @case({})
    @case({'node': WidgetNode(Entry(), Mock())})
    @case({'attr': XmlAttr('text')})
    @case({'node': Node(Mock()), 'attr': XmlAttr('text')})
    @case({'node': WidgetNode(Entry(), Mock()), 'attr': XmlAttr('some_property')})
    def test_false_for_bad_arguments(self, args: dict):
        rule = VariableTwowaysRule(Entry, 'text', 'textvariable')

        actual = rule.suitable(**args)

        msg = 'should return False for bad arguments'
        self.assertFalse(actual, msg)