from unittest import TestCase, main
from unittest.mock import Mock, call
from tkinter import Variable
from pyviews.testing import case
from tkviews.core.binding import VariableTarget, VariableBinding

class TestVariableTarget(TestCase):
    @case(1)
    @case('value')
    @case(None)
    @case([1, 'str'])
    def test_on_change_set_var(self, value):
        var = Variable()
        target = VariableTarget(var)

        target.on_change(value)

        msg = 'on_change set value to variable'
        self.assertEqual(var.get(), value, msg)

class TestVariableBinding(TestCase):
    @case(1)
    @case('value')
    @case(None)
    @case([1, 'str'])
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
