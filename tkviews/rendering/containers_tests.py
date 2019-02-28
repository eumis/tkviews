'''Containers rendering pipeline tests'''

# pylint: disable=C0111,C0103

from math import floor
from unittest import TestCase
from unittest.mock import Mock, call, patch
from pyviews.testing import case
from tkviews.node import Container, View, For, If
from . import containers
from .containers import render_container_children
from .containers import render_view_children, rerender_on_view_change
from .containers import render_for_items, rerender_on_items_change
from .containers import get_if_setup, render_if, subscribe_to_condition_change

class render_container_children_tests(TestCase):
    @patch(containers.__name__ + '.render_children')
    @patch(containers.__name__ + '.InheritedDict')
    @case([])
    @case(['item1'])
    @case(['item1', 'item2'])
    def test_renders_child(self, inherited_dict: Mock, render_children: Mock, nodes):
        xml_node = Mock(children=nodes)
        child_globals = Mock()
        inherited_dict.side_effect = lambda parent: child_globals
        node = Container(Mock(), xml_node)
        child_args = {
            'parent_node': node,
            'master': node.master,
            'node_globals': inherited_dict(node.node_globals),
            'node_styles': node.node_styles
        }

        render_container_children(node)

        msg = 'should render all xml children for every item'
        self.assertEqual(render_children.call_args, call(node, **child_args), msg)

class render_view_children_tests(TestCase):
    @patch(containers.__name__ + '.render_view')
    def test_renders_view(self, render_view: Mock):
        view_name = 'name'
        child = Mock()
        render_view.side_effect = lambda name, **args: child if name == view_name else None

        node = Mock(node_globals=None)
        node.set_content = Mock()
        node.name = view_name

        render_view_children(node)

        msg = 'should render view by node name and set result as view child'
        self.assertEqual(node.set_content.call_args, call(child), msg)

    @patch(containers.__name__ + '.render_view')
    @patch(containers.__name__ + '.InheritedDict')
    def test_renders_view_with_args(self, inherit_dict:Mock, render_view: Mock):
        view_name = 'name'
        inherit_dict.side_effect = lambda source: source
        render_view.side_effect = lambda name, **args: args

        node = Mock()
        node.node_globals = Mock()
        node.node_styles = Mock()
        node.set_content = Mock()
        node.master = Mock()
        node.name = view_name
        args = {
            'parent_node': node,
            'master': node.master,
            'node_globals': inherit_dict(node.node_globals),
            'node_styles': node.node_styles
        }

        render_view_children(node)

        msg = 'should render view by node name and set result as view child'
        self.assertEqual(node.set_content.call_args, call(args), msg)

    @patch(containers.__name__ + '.render_view')
    @case('')
    @case(None)
    def test_not_render_empty_view_name(self, render_view: Mock, view_name):
        node = Mock()
        node.set_content = Mock()
        node.name = view_name

        render_view_children(node)

        msg = 'should not render view if name is empty or None'
        self.assertFalse(node.set_content.called or render_view.called, msg)

class rerender_on_view_change_tests(TestCase):
    @patch(containers.__name__ + '.render_view_children')
    def test_renders_new_view(self, render_view_children: Mock):#pylint: disable=redefined-outer-name
        node = View(Mock(), Mock())
        node.destroy_children = Mock()
        view_name = 'name'
        args = {}

        rerender_on_view_change(node, **args)
        node.name = view_name

        msg = 'destroy_children should be called on view change'
        self.assertTrue(node.destroy_children.called, msg)

        msg = 'render_view_children should be called on view change'
        self.assertEqual(render_view_children.call_args, call(node, **args), msg)

    @patch(containers.__name__ + '.render_view')
    @case('')
    @case(None)
    def test_not_render_empty_name(self, render_view: Mock, view_name):
        node = View(Mock(), Mock())
        node.set_content = Mock()
        node.destroy_children = Mock()
        node.name = 'some name'

        rerender_on_view_change(node, **{})
        node.name = view_name

        msg = 'should not render in case name is not set or empty'
        self.assertFalse(render_view.called or node.set_content.called, msg)

    @patch(containers.__name__ + '.render_view_children')
    def test_not_rerender_same_view(self, render_view_children: Mock): #pylint: disable=redefined-outer-name
        node = View(Mock(), Mock())
        node.destroy_children = Mock()
        node.name = 'name'
        args = {}

        rerender_on_view_change(node, **args)
        node.name = node.name

        msg = 'destroy_children should be called on view change'
        self.assertFalse(node.destroy_children.called, msg)

        msg = 'render_view_children should be called on view change'
        self.assertFalse(render_view_children.called, msg)

class render_for_items_tests(TestCase):
    @patch(containers.__name__ + '.deps')
    @case([], [], [])
    @case(['item1'], ['node1'], ['node1'])
    @case(['item1'], ['node1', 'node2'], ['node1', 'node2'])
    @case(['item1', 'item2'], ['node1'], ['node1', 'node1'])
    @case(['item1', 'item2'], ['node1', 'node2'], ['node1', 'node2', 'node1', 'node2'])
    def test_renders_children_for_every_item(self, deps, items, nodes, expected_children):
        xml_node = Mock(children=nodes)
        node = For(Mock(), xml_node)
        node.items = items
        deps.render = lambda xml_node, **args: xml_node

        render_for_items(node)

        msg = 'should render all xml children for every item'
        self.assertEqual(node.children, expected_children, msg)

    @patch(containers.__name__ + '.deps')
    @case([], [], [])
    @case(['item1'], ['node1'], [(0, 'item1')])
    @case(['item1'], ['node1', 'node2'], [(0, 'item1'), (0, 'item1')])
    @case(['item1', 'item2'], ['node1'], [(0, 'item1'), (1, 'item2')])
    @case(['item1', 'item2'], ['node1', 'node2'],
          [(0, 'item1'), (0, 'item1'), (1, 'item2'), (1, 'item2')])
    def test_adds_item_and_index_to_globals(self, deps, items, nodes, expected_children):
        xml_node = Mock(children=nodes)
        node = For(Mock(), xml_node)
        node.items = items
        deps.render = lambda xml_node, **args: \
                      (args['node_globals']['index'], args['node_globals']['item'])

        render_for_items(node)

        msg = 'should add item and index to child globals'
        self.assertEqual(node.children, expected_children, msg)

class rerender_on_items_change_tests(TestCase):
    @patch(containers.__name__ + '.deps')
    @case(2, 4, 4)
    @case(2, 4, 2)
    @case(1, 4, 2)
    @case(4, 3, 0)
    @case(1, 3, 0)
    @case(3, 10, 1)
    def test_destroys_overflow_children(self, deps, xml_child_count, items_count, new_items_count):
        xml_node = Mock(children=[Mock() for i in range(xml_child_count)])
        node = For(Mock(), xml_node)
        node.items = [Mock() for i in range(items_count)]
        node.add_children([Mock(destroy=Mock(), node_globals={}) for i in range(xml_child_count * items_count)])
        deps.render = lambda xml_node, **args: Mock()

        to_destroy = node.children[xml_child_count * new_items_count:]
        to_left = node.children[:xml_child_count * new_items_count]

        rerender_on_items_change(node)
        node.items = [Mock() for i in range(new_items_count)]

        msg = 'should destroy overflow children'
        for child in to_destroy:
            self.assertTrue(child.destroy.called, msg)

        msg = 'should remove destroyed from children'
        self.assertEqual(node.children, to_left, msg)

    @patch(containers.__name__ + '.deps')
    @case(2, 4, 4)
    @case(2, 0, 4)
    @case(2, 4, 2)
    @case(2, 4, 6)
    @case(1, 4, 2)
    @case(4, 3, 0)
    @case(1, 3, 0)
    @case(3, 10, 11)
    def test_updates_items(self, deps, xml_child_count, items_count, new_items_count):
        xml_node = Mock(children=[Mock() for i in range(xml_child_count)])
        node = For(Mock(), xml_node)
        node.items = [Mock() for i in range(items_count)]
        node.add_children([Mock(destroy=Mock(), node_globals={}) for i in range(xml_child_count * items_count)])
        deps.render = lambda xml_node, **args: Mock()
        children_to_update = node.children[:xml_child_count * new_items_count]

        rerender_on_items_change(node)
        node.items = [Mock() for i in range(new_items_count)]

        msg = 'should update item in globals for every children'
        for i, child in enumerate(children_to_update):
            item = node.items[floor(i / xml_child_count)]
            self.assertEqual(child.node_globals['item'], item, msg)

    @patch(containers.__name__ + '.deps')
    @case(2, 4, 6)
    @case(2, 4, 10)
    @case(1, 4, 4)
    def test_creates_new_children(self, deps, xml_child_count, items_count, new_items_count):
        xml_node = Mock(children=[Mock() for i in range(xml_child_count)])
        node = For(Mock(), xml_node)
        node.items = [Mock() for i in range(items_count)]
        node.add_children([Mock(destroy=Mock(), node_globals={}) for i in range(xml_child_count * items_count)])
        deps.render = lambda xml_node, **args: Mock()

        rerender_on_items_change(node)
        node.items = [Mock() for i in range(new_items_count)]

        msg = 'should create new children'
        self.assertEqual(len(node.children), xml_child_count * new_items_count, msg)

class render_if_tests(TestCase):
    @patch(containers.__name__ + '.render_children')
    @case(True)
    @case(False)
    def test_renders_children(self, render_children, condition):
        render_children.reset_mock()
        node = If(Mock(), Mock())
        node.condition = condition

        render_if(node)

        msg = 'should render children if condition is True'
        self.assertEqual(render_children.called, condition, msg)

class subscribe_to_condition_change_tests(TestCase):
    @patch(containers.__name__ + '.render_children')
    def test_renders_children(self, render_children):
        node = If(Mock(), Mock())
        node.condition = False

        subscribe_to_condition_change(node, get_if_setup())
        node.condition = True

        msg = 'should render children if condition is changed to True'
        self.assertTrue(render_children.called, msg)

    @patch(containers.__name__ + '.render_children')
    def test_destroy_children(self, render_children): #pylint: disable=unused-argument
        node = Mock(destroy_children=Mock())
        node.condition = True

        subscribe_to_condition_change(node, get_if_setup())
        node.condition = False

        msg = 'should destroy children if condition is changed to False'
        self.assertTrue(node.destroy_children, msg)
