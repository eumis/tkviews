from unittest import TestCase, main
from unittest.mock import Mock, call
from pyviews.testing import case
from pyviews.core import ioc
from pyviews.core.xml import XmlNode
from tkviews.containers import Container, View, For, If

class ContainerTest(TestCase):
    def setUp(self):
        self.container = Container(None, None)
        self.container.property = None

    def test_set_attr(self):
        value = 'value'
        self.container.set_attr('property', value)

        msg = 'set_attr should set container property'
        self.assertEqual(self.container.property, value, msg)

class ViewTest(TestCase):
    def setUp(self):
        self.view = View(None, None)
        self.view.render_children = Mock()

    @case(True)
    @case(False)
    def test_name_change(self, is_rendered):
        self.view.render_children.reset_mock()
        self.view._rendered = is_rendered
        self.view.name = 'view'

        msg = 'render_children should be called on name change'
        self.assertEqual(self.view.render_children.called, is_rendered, msg)

    def test_same_name_passed(self):
        self.view._rendered = True
        view_name = 'view'
        self.view.name = view_name
        self.view.name = view_name

        msg = 'render_children should be called if passed name is not the same as curren'
        self.assertEqual(self.view.render_children.call_count, 1, msg)

class ForTest(TestCase):
    def setUp(self):
        self._child = Mock()
        self._child.destroy = Mock()
        self._child.globals = Mock()
        self._child.globals.__setitem__ = Mock(side_effect=lambda *args: None)
        self._render = Mock(return_value=self._child)
        with ioc.Scope('ForTest'):
            ioc.register_single('render', self._render)

    def _init_test(self, child_count=3):
        self._reset_mocks()
        return self._create_node(child_count)

    def _reset_mocks(self):
        self._render.reset_mock()
        self._child.reset_mock()

    def _create_node(self, child_count):
        xml_node = XmlNode('tkviews', 'For')
        for i in range(child_count):
            xml_node.children.append(XmlNode('tkviews', 'child'))
        node = For(None, xml_node)
        return (xml_node, node)

    @case([])
    @case(['asdf', 'qwer'])
    def test_items_shouldnt_trigger_render(self, items):
        node = self._init_test()[1]
        node.items = items

        msg = "initial items set shouldn't call render_children"
        self.assertFalse(self._render.called, msg)

    @ioc.scope('ForTest')
    @case([], 1)
    @case([1], 0)
    @case([1], 1)
    @case([1], 2)
    @case([1, 2], 0)
    @case([1, 2], 1)
    @case([1, 2], 4)
    def test_all_children_should_be_created(self, items, child_count):
        node = self._init_test(child_count)[1]
        node.items = items
        node.render_children()

        msg = 'all children should be created for every item'
        self.assertEqual(self._render.call_count, len(items) * child_count, msg)

    @ioc.scope('ForTest')
    @case([1], [2], 2)
    @case([1], [2], 1)
    @case([1, 2], [2], 1)
    @case([1, 2], [2], 2)
    @case([1, 2], [2, 3, 4], 5)
    @case([1, 2], [2, 3, 4], 1)
    def test_children_should_be_updated(self, items, new_items, child_count):
        node = self._init_test(child_count)[1]
        node.items = items
        node.render_children()
        self._child.reset_mock()

        node.items = new_items

        count = min(len(items), len(new_items)) * child_count
        calls = [call('item', new_items[int(i / child_count)]) for i in range(0, count)]
        set_item_mock = self._child.globals.__setitem__

        msg = 'children should be updated when items are updated'
        self.assertEqual(set_item_mock.call_args_list, calls, msg)

    @ioc.scope('ForTest')
    @case([1], [2], 2)
    @case([1], [2], 1)
    @case([1, 2], [2], 1)
    @case([1, 2], [2], 2)
    @case([1, 2], [2, 3, 4], 5)
    @case([1, 2], [2, 3, 4], 1)
    @case([1, 2, 3, 4, 5, 6], [2, 3], 1)
    @case([1, 2, 3, 4, 5, 6], [2, 3], 3)
    def test_overflow_children_should_be_removed(self, items, new_items, child_count):
        node = self._init_test(child_count)[1]
        node.items = items
        node.render_children()
        self._child.reset_mock()

        node.items = new_items

        items_count = len(items)
        new_count = len(new_items)
        count = (items_count - new_count) * child_count \
                if items_count > new_count else 0

        msg = 'overflow children should be removed when items are updated'
        self.assertEqual(self._child.destroy.call_count, count, msg)

    @ioc.scope('ForTest')
    @case([1], [2], 2)
    @case([1], [2], 1)
    @case([1, 2], [2], 1)
    @case([1, 2], [2], 2)
    @case([1, 2], [2, 3, 4], 5)
    @case([1, 2], [2, 3, 4], 1)
    @case([2, 3], [1, 2, 3, 4, 5, 6], 1)
    @case([2, 3], [1, 2, 3, 4, 5, 6], 3)
    def test_new_children_should_be_created(self, items, new_items, child_count):
        node = self._init_test(child_count)[1]
        node.items = items
        node.render_children()
        self._render.reset_mock()

        node.items = new_items

        items_count = len(items)
        new_count = len(new_items)
        count = (new_count - items_count) * child_count \
                if new_count > items_count else 0

        msg = 'new children should be created new items'
        self.assertEqual(self._render.call_count, count, msg)

class IfTest(TestCase):
    def setUp(self):
        self._setup_ioc()
        self._setup_node()

    def _setup_ioc(self):
        self._child = Mock()
        self._child.destroy = Mock()
        self._child.globals = Mock()
        self._child.globals.__setitem__ = Mock(side_effect=lambda *args: None)
        self._parse = Mock(return_value=self._child)
        with ioc.Scope('IfTest'):
            ioc.register_single('render', self._parse)

    def _setup_node(self):
        xml_node = XmlNode('tkviews', 'If')
        xml_node.children.append(XmlNode('tkviews', 'child'))
        self.node = If(None, xml_node)

    def test_default_condition_false(self):
        msg = 'default "condition" value should be False'
        self.assertFalse(self.node.condition, msg)

    @ioc.scope('IfTest')
    def test_init_setup_shouldnt_trigger_render(self):
        self.node.condition = True
        self.node.condition = False

        msg = "initial items set shouldn't call render_children"
        self.assertFalse(self._parse.called, msg)
        self.assertFalse(self._child.destroy.called, msg)

    @ioc.scope('IfTest')
    @case(True)
    @case(False)
    def test_same_condition_shouldnt_trigger_render(self, value):
        self.node.condition = value
        self.node.render_children()
        self._parse.reset_mock()
        self._child.reset_mock()

        self.node.condition = value

        msg = "same condition value shouldn't trigger parsing"
        self.assertFalse(self._parse.called, msg)
        self.assertFalse(self._child.destroy.called, msg)

    @ioc.scope('IfTest')
    def test_true_should_trigger_render(self):
        self.node.render_children()
        self._parse.reset_mock()
        self._child.reset_mock()

        self.node.condition = True

        msg = "True value shouldn't trigger parsing"
        self.assertTrue(self._parse.called, msg)

    @ioc.scope('IfTest')
    def test_false_should_trigger_destroy(self):
        self.node.condition = True
        self.node.render_children()
        self._parse.reset_mock()
        self._child.reset_mock()

        self.node.condition = False

        msg = "False value should destroy children"
        self.assertTrue(self._child.destroy.called, msg)

if __name__ == '__main__':
    main()
