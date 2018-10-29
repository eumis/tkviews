from math import floor
from unittest import TestCase, main
from unittest.mock import Mock, call, patch
from pyviews import NodeSetup
from pyviews.testing import case
from pyviews.core import ioc
from pyviews.core.xml import XmlNode
from tkviews.core.containers import Container, View, For, If
from tkviews.setup.containers import render_view_children, rerender_on_view_change
from tkviews.setup.containers import get_for_setup, render_for_items, rerender_on_items_change
from tkviews.setup.containers import get_if_setup, render_if, subscribe_to_condition_change

class ViewTest(TestCase):
    def setUp(self):
        self.container = Container(None, None)
        self.container.property = None

    @patch('tkviews.setup.containers.get_view_root')
    @patch('tkviews.setup.containers.deps')
    def test_render_view_children_should_render_child(self, deps: Mock, get_view_root: Mock):
        view_name = 'name'
        view_root = Mock()
        get_view_root.side_effect = lambda name: view_root if name == view_name else None

        child = Mock()
        deps.render = Mock(side_effect=lambda r, **args: child if r == view_root else None)

        node = Mock()
        node.set_content = Mock()
        node.name = view_name

        render_view_children(node, node_setup=NodeSetup(get_child_args=Mock(return_value={})))

        msg = 'render_view_children should render view by node name and set result as view child'
        self.assertEqual(node.set_content.call_args, call(child), msg)

    @patch('tkviews.setup.containers.render_view_children')
    def test_rerender_on_view_change_should_render_new_view(self, render_view_children: Mock):
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

    @patch('tkviews.setup.containers.render_view_children')
    def test_rerender_on_view_change_should_not_rerender_same_view(self, render_view_children: Mock):
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

class ForTest(TestCase):
    @patch('tkviews.setup.containers.deps')
    @case([], [], [])
    @case(['item1'], ['node1'], ['node1'])
    @case(['item1'], ['node1', 'node2'], ['node1', 'node2'])
    @case(['item1', 'item2'], ['node1'], ['node1', 'node1'])
    @case(['item1', 'item2'], ['node1', 'node2'], ['node1', 'node2', 'node1', 'node2'])
    def test_render_for_items_should_render_xml_nodes(self, deps, items, nodes, expected_children):
        xml_node = Mock(children=nodes)
        node = For(Mock(), xml_node)
        node.items = items
        deps.render = lambda xml_node, **args: xml_node

        render_for_items(node, get_for_setup())

        msg = 'render_for_items should render all xml children for every item'
        self.assertEqual(node.children, expected_children, msg)

    @patch('tkviews.setup.containers.deps')
    @case([], [], [])
    @case(['item1'], ['node1'], [(0, 'item1')])
    @case(['item1'], ['node1', 'node2'], [(0, 'item1'), (0, 'item1')])
    @case(['item1', 'item2'], ['node1'], [(0, 'item1'), (1, 'item2')])
    @case(['item1', 'item2'], ['node1', 'node2'],
          [(0, 'item1'), (0, 'item1'), (1, 'item2'), (1, 'item2')])
    def test_render_for_items_should_add_item_and_index_to_globals(self, deps, items, nodes, expected_children):
        xml_node = Mock(children=nodes)
        node = For(Mock(), xml_node)
        node.items = items
        deps.render = lambda xml_node, **args: (args['node_globals']['index'], args['node_globals']['item'])

        render_for_items(node, get_for_setup())

        msg = 'render_for_items should add item and index to child globals'
        self.assertEqual(node.children, expected_children, msg)

    @patch('tkviews.setup.containers.deps')
    @case(2, 4, 4)
    @case(2, 4, 2)
    @case(1, 4, 2)
    @case(4, 3, 0)
    @case(1, 3, 0)
    @case(3, 10, 1)
    def test_rerender_on_items_change_destroys(self, deps, xml_child_count, items_count, new_items_count):
        xml_node = Mock(children=[Mock() for i in range(xml_child_count)])
        node = For(Mock(), xml_node)
        node.items = [Mock() for i in range(items_count)]
        node.add_children([Mock(destroy=Mock(),globals={}) for i in range(xml_child_count * items_count)])
        deps.render = lambda xml_node, **args: Mock()

        to_destroy = node.children[xml_child_count * new_items_count:]
        to_left = node.children[:xml_child_count * new_items_count]

        rerender_on_items_change(node, node_setup=get_for_setup())
        node.items = [Mock() for i in range(new_items_count)]

        msg = 'rerender_on_items_change should destroy overflow nodes'
        for child in to_destroy:
            self.assertTrue(child.destroy.called, msg)

        msg = 'rerender_on_items_change should removed destroyed from children'
        self.assertEqual(node.children, to_left, msg)

    @patch('tkviews.setup.containers.deps')
    @case(2, 4, 4)
    @case(2, 0, 4)
    @case(2, 4, 2)
    @case(2, 4, 6)
    @case(1, 4, 2)
    @case(4, 3, 0)
    @case(1, 3, 0)
    @case(3, 10, 11)
    def test_rerender_on_items_change_updates_item(self, deps, xml_child_count, items_count, new_items_count):
        xml_node = Mock(children=[Mock() for i in range(xml_child_count)])
        node = For(Mock(), xml_node)
        node.items = [Mock() for i in range(items_count)]
        node.add_children([Mock(destroy=Mock(), globals={}) for i in range(xml_child_count * items_count)])
        deps.render = lambda xml_node, **args: Mock()
        children_to_update = node.children[:xml_child_count * new_items_count]

        rerender_on_items_change(node, node_setup=get_for_setup())
        node.items = [Mock() for i in range(new_items_count)]

        msg = 'rerender_on_items_change should update item in globals for children'
        for i, child in enumerate(children_to_update):
            item = node.items[floor(i / xml_child_count)]
            self.assertEqual(child.globals['item'], item, msg)

    @patch('tkviews.setup.containers.deps')
    @case(2, 4, 6)
    @case(2, 4, 10)
    @case(1, 4, 4)
    def test_rerender_on_items_change_creates_new(self, deps, xml_child_count, items_count, new_items_count):
        xml_node = Mock(children=[Mock() for i in range(xml_child_count)])
        node = For(Mock(), xml_node)
        node.items = [Mock() for i in range(items_count)]
        node.add_children([Mock(destroy=Mock(), globals={}) for i in range(xml_child_count * items_count)])
        deps.render = lambda xml_node, **args: Mock()

        rerender_on_items_change(node, node_setup=get_for_setup())
        node.items = [Mock() for i in range(new_items_count)]

        msg = 'rerender_on_items_change should create new children'
        self.assertEqual(len(node.children), xml_child_count * new_items_count, msg)

class IfTest(TestCase):
    @patch('tkviews.setup.containers.render_children')
    @case(True)
    @case(False)
    def test_render_if_renders(self, render_children, condition):
        render_children.reset_mock()
        node = If(Mock(), Mock())
        node.condition = condition

        render_if(node, get_if_setup())

        msg = 'render_if should render children if condition is True'
        self.assertEqual(render_children.called, condition, msg)

    @patch('tkviews.setup.containers.render_children')
    def test_subscribe_to_condition_change_should_render_children(self, render_children):
        node = If(Mock(), Mock())
        node.condition = False

        subscribe_to_condition_change(node, get_if_setup())
        node.condition = True

        msg = 'subscribe_to_condition_change should render children if condition is changed to True'
        self.assertTrue(render_children.called, msg)

    @patch('tkviews.setup.containers.render_children')
    def test_subscribe_to_condition_change_should_destroy_children(self, render_children):
        node = Mock(destroy_children=Mock())
        node.condition = True

        subscribe_to_condition_change(node, get_if_setup())
        node.condition = False

        msg = 'subscribe_to_condition_change should destroy children if condition is changed to False'
        self.assertTrue(node.destroy_children, msg)

if __name__ == '__main__':
    main()
