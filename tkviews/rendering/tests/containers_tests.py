from math import floor
from unittest.mock import Mock, call, patch

from pytest import mark
from tkviews.node import Container, View, For, If
from tkviews.rendering import containers
from tkviews.rendering.common import TkRenderingContext
from tkviews.rendering.containers import render_container_children
from tkviews.rendering.containers import render_view_children, rerender_on_view_change
from tkviews.rendering.containers import render_for_items, rerender_on_items_change
from tkviews.rendering.containers import render_if, subscribe_to_condition_change


@mark.parametrize('nodes', [
    [],
    ['item1'],
    ['item1', 'item2']
])
def test_render_container_children(nodes):
    """should render all xml children for every item"""
    with patch(containers.__name__ + '.render_children') as render_children:
        with patch(containers.__name__ + '.InheritedDict') as InheritedDict:
            xml_node = Mock(children=nodes)
            child_globals = Mock()
            InheritedDict.side_effect = lambda parent: child_globals
            node = Container(Mock(), xml_node)
            child_args = {
                'parent_node': node,
                'master': node.master,
                'node_globals': InheritedDict(node.node_globals),
                'node_styles': node.node_styles
            }

            render_container_children(node, TkRenderingContext())

        assert render_children.call_args == call(node, TkRenderingContext(child_args))


class ViewRenderingTests:
    """render_view_children() tests"""

    @staticmethod
    @patch(containers.__name__ + '.render_view')
    def test_renders_view(render_view: Mock):
        """should render view by node name and set result as view child"""
        view_name = 'name'
        child = Mock()
        render_view.side_effect = lambda name, ctx: child if name == view_name else None

        node = Mock(node_globals=None)
        node.set_content = Mock()
        node.name = view_name

        render_view_children(node, TkRenderingContext())

        assert node.set_content.call_args == call(child)

    @staticmethod
    @patch(containers.__name__ + '.render_view')
    @patch(containers.__name__ + '.InheritedDict')
    def test_renders_view_with_args(inherit_dict: Mock, render_view: Mock):
        """should render view by node name and set result as view child"""
        view_name = 'name'
        inherit_dict.side_effect = lambda source: source
        render_view.side_effect = lambda name, a: a

        node = Mock()
        node.node_globals = Mock()
        node.node_styles = Mock()
        node.set_content = Mock()
        node.master = Mock()
        node.name = view_name
        args = TkRenderingContext({
            'parent_node': node,
            'master': node.master,
            'node_globals': inherit_dict(node.node_globals),
            'node_styles': node.node_styles
        })

        render_view_children(node, TkRenderingContext())

        assert node.set_content.call_args == call(args)

    @staticmethod
    @mark.parametrize('view_name', ['', None])
    def test_not_render_empty_view_name(view_name):
        """should not render view if name is empty or None"""
        node = Mock()
        node.set_content = Mock()
        node.name = view_name

        with patch(containers.__name__ + '.render_view') as render_view:
            render_view_children(node, TkRenderingContext())

            assert not (node.set_content.called or render_view.called)


class RenderViewChangeTests:
    """rerender_on_view_change tests"""

    @staticmethod
    @patch(containers.__name__ + '.render_view_children')
    def test_renders_new_view(render_view_children: Mock):
        """render_view_children should be called on view change"""
        node = View(Mock(), Mock())
        node.destroy_children = Mock()
        view_name = 'name'
        context = TkRenderingContext()

        rerender_on_view_change(node, context)
        node.name = view_name

        assert node.destroy_children.called
        assert render_view_children.call_args == call(node, context)

    @staticmethod
    @mark.parametrize('view_name', ['', None])
    def test_not_render_empty_name(view_name):
        """should not render in case name is not set or empty"""
        node = View(Mock(), Mock())
        node.set_content = Mock()
        node.destroy_children = Mock()
        node.name = 'some name'

        with patch(containers.__name__ + '.render_view') as render_view:
            rerender_on_view_change(node, TkRenderingContext())
            node.name = view_name

            assert not (render_view.called or node.set_content.called)

    @staticmethod
    @patch(containers.__name__ + '.render_view_children')
    def test_not_rerender_same_view(render_view_children: Mock):
        """render_view_children should be called on view change"""
        node = View(Mock(), Mock())
        node.destroy_children = Mock()
        node.name = 'name'
        args = {}

        rerender_on_view_change(node, TkRenderingContext(args))
        node.name = node.name

        assert not node.destroy_children.called
        assert not render_view_children.called


class RenderForItemsTests:
    """render_for_items tests"""

    @staticmethod
    @mark.parametrize('items, nodes, expected_children', [
        ([], [], []),
        (['item1'], ['node1'], ['node1']),
        (['item1'], ['node1', 'node2'], ['node1', 'node2']),
        (['item1', 'item2'], ['node1'], ['node1', 'node1']),
        (['item1', 'item2'], ['node1', 'node2'], ['node1', 'node2', 'node1', 'node2'])
    ])
    def test_renders_children_for_every_item(items, nodes, expected_children):
        """should render all xml children for every item"""
        with patch(containers.__name__ + '.render') as render:
            xml_node = Mock(children=nodes)
            node = For(Mock(), xml_node)
            node.items = items
            render.side_effect = lambda xmlnode, ctx: xmlnode

            render_for_items(node, TkRenderingContext())

            assert node.children == expected_children

    @staticmethod
    @mark.parametrize('items, nodes, expected_children', [
        ([], [], []),
        (['item1'], ['node1'], [(0, 'item1')]),
        (['item1'], ['node1', 'node2'], [(0, 'item1'), (0, 'item1')]),
        (['item1', 'item2'], ['node1'], [(0, 'item1'), (1, 'item2')]),
        (['item1', 'item2'],
         ['node1', 'node2'],
         [(0, 'item1'), (0, 'item1'), (1, 'item2'), (1, 'item2')])
    ])
    def test_adds_item_and_index_to_globals(items, nodes, expected_children):
        """should add item and index to child globals"""
        with patch(containers.__name__ + '.render') as render:
            xml_node = Mock(children=nodes)
            node = For(Mock(), xml_node)
            node.items = items
            render.side_effect = lambda xmlnode, ctx: \
                (ctx.node_globals['index'], ctx.node_globals['item'])

            render_for_items(node, TkRenderingContext())

            assert node.children == expected_children


class RenderOnItemsChangeTests:
    """render_on_items_change() tests"""

    @staticmethod
    @mark.parametrize('xml_child_count, items_count, new_items_count', [
        (2, 4, 4),
        (2, 4, 2),
        (1, 4, 2),
        (4, 3, 0),
        (1, 3, 0),
        (3, 10, 1)
    ])
    def test_destroys_overflow_children(xml_child_count, items_count, new_items_count):
        """should destroy and remove overflow children"""
        with patch(containers.__name__ + '.render') as render:
            xml_node = Mock(children=[Mock() for _ in range(xml_child_count)])
            node = For(Mock(), xml_node)
            node.items = [Mock() for _ in range(items_count)]
            node.add_children([Mock(destroy=Mock(), node_globals={}) for _ in range(xml_child_count * items_count)])
            render.side_effect = lambda xmlnode, **args: Mock()

            to_destroy = node.children[xml_child_count * new_items_count:]
            to_left = node.children[:xml_child_count * new_items_count]

            rerender_on_items_change(node, TkRenderingContext())
            node.items = [Mock() for _ in range(new_items_count)]

            for child in to_destroy:
                assert child.destroy.called
            assert node.children == to_left

    @staticmethod
    @mark.parametrize('xml_child_count, items_count, new_items_count', [
        (2, 4, 4),
        (2, 0, 4),
        (2, 4, 2),
        (2, 4, 6),
        (1, 4, 2),
        (4, 3, 0),
        (1, 3, 0),
        (3, 10, 11)
    ])
    def test_updates_items(xml_child_count, items_count, new_items_count):
        """should update item in globals for every children"""
        with patch(containers.__name__ + '.render') as render:
            xml_node = Mock(children=[Mock() for _ in range(xml_child_count)])
            node = For(Mock(), xml_node)
            node.items = [Mock() for _ in range(items_count)]
            node.add_children([Mock(destroy=Mock(), node_globals={}) for _ in range(xml_child_count * items_count)])
            render.side_effect = lambda xmlnode, args: Mock()
            children_to_update = node.children[:xml_child_count * new_items_count]

            rerender_on_items_change(node, TkRenderingContext())
            node.items = [Mock() for _ in range(new_items_count)]

            for i, child in enumerate(children_to_update):
                item = node.items[floor(i / xml_child_count)]
                assert child.node_globals['item'] == item

    @staticmethod
    @mark.parametrize('xml_child_count, items_count, new_items_count', [
        (2, 4, 6),
        (2, 4, 10),
        (1, 4, 4)
    ])
    def test_creates_new_children(xml_child_count, items_count, new_items_count):
        """should create new children"""
        with patch(containers.__name__ + '.render') as render:
            xml_node = Mock(children=[Mock() for _ in range(xml_child_count)])
            node = For(Mock(), xml_node)
            node.items = [Mock() for _ in range(items_count)]
            node.add_children([Mock(destroy=Mock(), node_globals={}) for _ in range(xml_child_count * items_count)])
            render.side_effect = lambda xmlnode, args: Mock()

            rerender_on_items_change(node, TkRenderingContext())
            node.items = [Mock() for _ in range(new_items_count)]

            assert len(node.children) == xml_child_count * new_items_count


@mark.parametrize('condition', [True, False])
def test_render_if(condition):
    """should render children if condition is True"""
    with patch(containers.__name__ + '.render_children') as render_children:
        node = If(Mock(), Mock())
        node.condition = condition

        render_if(node, TkRenderingContext())

        assert render_children.called == condition


class SubscribeToConditionTests:
    """subscribe_to_condition_change() tests"""

    @staticmethod
    def test_renders_children():
        """should render children if condition is changed to True"""
        with patch(containers.__name__ + '.render_children') as render_children:
            node = If(Mock(), Mock())
            node.condition = False

            subscribe_to_condition_change(node, TkRenderingContext())
            node.condition = True

            assert render_children.called

    @staticmethod
    def test_destroy_children():
        """should destroy children if condition is changed to False"""
        with patch(containers.__name__ + '.render_children'):
            node = Mock(destroy_children=Mock())
            node.condition = True

            subscribe_to_condition_change(node, TkRenderingContext())
            node.condition = False

            assert node.destroy_children
