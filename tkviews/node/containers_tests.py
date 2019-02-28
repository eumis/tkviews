# pylint: disable=C0111,C0103

from unittest import TestCase
from unittest.mock import Mock, call
from pyviews.testing import case
from pyviews.core import XmlNode
from .containers import View, For, If

class View_init_tests(TestCase):
    def test_name_is_none_by_default(self):
        view = View(Mock(), Mock())

        msg = 'name should be None by default'
        self.assertIsNone(view.name, msg)

class View_name_changed_tests(TestCase):
    @case(None, 'name')
    @case('name', 'another name')
    def test_called_on_name_changed(self, old_name, new_name):
        view = View(Mock(), Mock())
        view.name = old_name
        view.name_changed = Mock()

        view.name = new_name

        msg = 'should call name_changed on name change'
        self.assertEqual(view.name_changed.call_args, call(view, new_name, old_name), msg)

class View_set_content_tests(TestCase):
    @case(XmlNode('', ''))
    def test_sets_children(self, content_root: XmlNode):
        view = View(Mock(), Mock())

        view.set_content(content_root)

        msg = 'should set content as children nodes'
        self.assertEqual(view.children, [content_root], msg)

class For_items_changed_tests(TestCase):
    @case([], [Mock()])
    @case([Mock()], [])
    @case([Mock()], [Mock(), Mock()])
    def test_called_on_items_changed(self, old_items, new_items):
        node = For(Mock(), Mock())
        node.items = old_items
        node.items_changed = Mock()

        node.items = new_items

        msg = 'should call items_changed on items change'
        self.assertEqual(node.items_changed.call_args, call(node, new_items, old_items), msg)

class If_init_tests(TestCase):
    def test_condition_is_false_by_default(self):
        node = If(Mock(), Mock())

        msg = 'condition should be False by default'
        self.assertFalse(node.condition, msg)

class If_condition_changed_tests(TestCase):
    @case(False, True)
    @case(True, False)
    def test_called_on_condition_changed(self, old_condition, new_condition):
        node = If(Mock(), Mock())
        node.condition = old_condition
        node.condition_changed = Mock()

        node.condition = new_condition

        msg = 'should call condition_changed on condition change'
        self.assertEqual(node.condition_changed.call_args,
                         call(node, new_condition, old_condition),
                         msg)
