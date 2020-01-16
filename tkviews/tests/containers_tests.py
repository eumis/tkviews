from math import floor
from unittest.mock import Mock, call, patch

from injectool import add_singleton
from pytest import mark, fixture
from pyviews.core import XmlNode, Node, InheritedDict
from pyviews.rendering import render
from pyviews.rendering.views import render_view
from rx import of

from tkviews import containers
from tkviews.containers import View, For, If, Container, render_container_children, render_view_content, \
    rerender_on_view_change, render_for_items, rerender_on_items_change, render_if, subscribe_to_condition_change
from tkviews.core.common import TkRenderingContext


class TestNode(Node):
    def __init__(self, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self.node_styles = InheritedDict(node_styles)


@mark.usefixtures('container_fixture')
@mark.parametrize('nodes_count', [1, 2, 5])
def test_render_container_children(nodes_count):
    """should render all xml children for every item"""
    render_mock = Mock()
    add_singleton(render, render_mock)
    with patch(containers.__name__ + '.InheritedDict') as InheritedDict:
        InheritedDict.side_effect = lambda parent: {'source': parent} if parent else parent
        xml_node = Mock(children=[Mock() for _ in range(nodes_count)])
        node = Container(Mock(), xml_node)
        context = TkRenderingContext({'node': node})

        render_container_children(node, context)

        for actual_call, child_xml_node in zip(render_mock.call_args_list, xml_node.children):
            child_context = TkRenderingContext({
                'parent_node': node,
                'master': node.master,
                'node_globals': InheritedDict(node.node_globals),
                'node_styles': InheritedDict(node.node_styles),
                'xml_node': child_xml_node
            })
            assert actual_call == call(child_context)


class ViewTests:
    """View node tests"""

    @staticmethod
    def test_init():
        """__init__() should sent name to None"""
        view = View(Mock(), Mock())

        assert view.name is None

    @staticmethod
    @mark.parametrize('old_name, new_name', [
        (None, 'name'),
        ('name', 'another name')
    ])
    def test_name_changed(old_name, new_name):
        """name_changed() should be called on name change"""
        view = View(Mock(), Mock())
        view.name = old_name
        view.name_changed = Mock()

        view.name = new_name

        assert view.name_changed.call_args == call(view, new_name, old_name)

    @staticmethod
    @mark.parametrize('content_root', [
        (Node(XmlNode('', '')))
    ])
    def test_set_content(content_root: Node):
        """should set content as children nodes"""
        view = View(Mock(), Mock())

        view.set_content(content_root)

        assert view.children == [content_root]


@fixture
def view_fixture(request):
    render_view_mock = Mock()
    add_singleton(render_view, render_view_mock)

    view = View(Mock(), Mock(), node_globals=InheritedDict({'key': 'value'}),
                node_styles=InheritedDict({'style': 'style'}))
    view.name = 'view'

    request.cls.render_view = render_view_mock
    request.cls.view = view


@mark.usefixtures('container_fixture', 'view_fixture')
class ViewRenderingTests:
    """render_view_children() tests"""

    def test_renders_view(self):
        """should render view by node name and set result as view child"""
        child = Mock()
        self.render_view.side_effect = lambda name, ctx: of(child) if name == self.view.name else None

        render_view_content(self.view, TkRenderingContext())

        assert self.view.children == [child]

    def test_renders_view_with_context(self):
        """should render view by node name and set result as view child"""
        actual = TkRenderingContext()
        self.render_view.side_effect = lambda name, ctx: of(actual.update(**ctx))

        render_view_content(self.view, TkRenderingContext())

        assert actual.master == self.view.master
        assert actual.parent_node == self.view
        assert actual.node_globals.to_dictionary() == self.view.node_globals.to_dictionary()
        assert actual.node_styles.to_dictionary() == self.view.node_styles.to_dictionary()

    @mark.parametrize('view_name', ['', None])
    def test_not_render_empty_view_name(self, view_name):
        """should not render view if name is empty or None"""
        self.view.name = view_name

        render_view_content(self.view, TkRenderingContext())

        assert self.view.children == []

    def test_handles_new_view(self):
        """render_view_children should be called on view change"""
        self.view.add_child(Mock())
        self.render_view.side_effect = lambda name, ctx: of({'name': name})
        new_view = 'new view'

        rerender_on_view_change(self.view, TkRenderingContext())
        self.view.name = new_view

        assert self.view.children == [{'name': new_view}]

    @mark.parametrize('view_name', ['', None])
    def test_not_render_empty_new_name(self, view_name):
        """should not render in case name is not set or empty"""
        rerender_on_view_change(self.view, TkRenderingContext())
        self.view.name = view_name

        assert self.view.children == []

    def test_not_rerender_same_view(self):
        """render_view_children should be called on view change"""
        current_content = Mock()
        self.view.add_child(current_content)
        rerender_on_view_change(self.view, TkRenderingContext())
        self.view.name = self.view.name

        assert self.view.children == [current_content]


class IfTests:
    """If node tests"""

    @staticmethod
    @mark.parametrize('old_condition, new_condition', [
        (False, True),
        (True, False)
    ])
    def test_condition_changed_called(old_condition, new_condition):
        """condition_changed should be called on condition change"""
        node = If(Mock(), Mock())
        node.condition = old_condition
        node.condition_changed = Mock()

        node.condition = new_condition

        assert node.condition_changed.call_args == call(node, new_condition, old_condition)


@fixture
def if_fixture(request):
    render_mock = Mock()
    render_mock.side_effect = lambda ctx: of(
        TestNode(ctx.xml_node, node_globals=ctx.node_globals, node_styles=ctx.node_styles))
    add_singleton(render, render_mock)

    if_node = If(Mock(), XmlNode('tkviews', 'If'), node_globals=InheritedDict({'key': 'value'}),
                 node_styles=InheritedDict({'style': 'style'}))

    request.cls.render = render_mock
    request.cls.if_node = if_node


@mark.usefixtures('container_fixture', 'if_fixture')
class IfRenderingTests:
    @mark.parametrize('condition, children_count', [
        (True, 0), (False, 0),
        (True, 1), (False, 1),
        (True, 5), (False, 5)
    ])
    def test_render_if(self, condition, children_count):
        """should render children if condition is True"""
        self.if_node._xml_node = self.if_node._xml_node._replace(children=[Mock() for _ in range(children_count)])
        self.if_node.condition = condition
        expected_children = self.if_node.xml_node.children if condition else []

        render_if(self.if_node, TkRenderingContext())

        assert [child.xml_node for child in self.if_node.children] == expected_children

    @mark.parametrize('children_count', [0, 1, 5])
    def test_renders_children(self, children_count):
        """should render children if condition is changed to True"""
        self.if_node.xml_node.children.extend([Mock() for _ in range(children_count)])

        subscribe_to_condition_change(self.if_node, TkRenderingContext())
        self.if_node.condition = True

        assert [child.xml_node for child in self.if_node.children] == self.if_node.xml_node.children

    @mark.parametrize('children_count', [0, 1, 5])
    def test_destroy_children(self, children_count):
        """should destroy children if condition is changed to False"""
        self.if_node.condition = True
        self.if_node.add_children([Mock() for _ in range(children_count)])

        subscribe_to_condition_change(self.if_node, TkRenderingContext())
        self.if_node.condition = False

        assert self.if_node.children == []


class ForTests:
    """For node tests"""

    @staticmethod
    def test_init():
        """condition should be False by default"""
        node = If(Mock(), Mock())

        assert not node.condition

    @staticmethod
    @mark.parametrize('old_items, new_items', [
        ([], [Mock()]),
        ([Mock()], []),
        ([Mock()], [Mock(), Mock()])
    ])
    def test_called_on_items_changed(old_items, new_items):
        """items_changed() should be called on items change"""
        node = For(Mock(), Mock())
        node.items = old_items
        node.items_changed = Mock()

        node.items = new_items

        assert node.items_changed.call_args == call(node, new_items, old_items)


@fixture
def for_fixture(request):
    render_mock = Mock()
    render_mock.side_effect = lambda ctx: of(TestNode(ctx.xml_node, node_globals=ctx.node_globals,
                                                      node_styles=ctx.node_styles))
    add_singleton(render, render_mock)

    for_node = For(Mock(), XmlNode('tkviews', 'For'), node_globals=InheritedDict({'key': 'value'}),
                   node_styles=InheritedDict({'style': 'style'}))

    request.cls.render = render_mock
    request.cls.for_node = for_node


@mark.usefixtures('container_fixture', 'for_fixture')
class RenderForItemsTests:
    """render_for_items tests"""

    @mark.parametrize('items, xml_children', [
        ([], []),
        (['item1'], ['node1']),
        (['item1'], ['node1', 'node2']),
        (['item1', 'item2'], ['node1']),
        (['item1', 'item2'], ['node1', 'node2'])
    ])
    def test_renders_children_for_every_item(self, items, xml_children):
        """should render all xml children for every item"""
        self.for_node.items = items
        self.for_node._xml_node = self.for_node._xml_node._replace(children=xml_children)

        render_for_items(self.for_node, TkRenderingContext())
        actual = iter(self.for_node.children)

        for index, item in enumerate(items):
            for xml_node in xml_children:
                child = next(actual)

                assert child.xml_node == xml_node
                assert child.node_globals.to_dictionary() == {'index': index, 'item': item,
                                                              **self.for_node.node_globals.to_dictionary(),
                                                              'node': child}
                assert child.node_styles.to_dictionary() == self.for_node.node_styles.to_dictionary()

    @mark.parametrize('items, xml_children, new_items', [
        (['item1'], ['node1'], ['item2']),
        (['item1'], ['node1'], ['item1', 'item2']),
        (['item1'], ['node1', 'node2'], ['item2']),
        (['item1'], ['node1', 'node2'], ['item1', 'item2']),
        (['item1', 'item2'], ['node1'], ['item2', 'item3']),
        (['item1', 'item2'], ['node1'], ['item1']),
        (['item1', 'item2'], ['node1'], ['item4']),
        (['item1', 'item2'], ['node1'], []),
        (['item1', 'item2'], ['node1', 'node2'], ['item1', 'item2', 'item3'])
    ])
    def test_renders_new_items(self, items, xml_children, new_items):
        """should render all xml children for every item"""
        self.for_node.items = items
        self.for_node._xml_node = self.for_node._xml_node._replace(children=xml_children)
        render_for_items(self.for_node, TkRenderingContext())

        rerender_on_items_change(self.for_node, TkRenderingContext())
        self.for_node.items = new_items
        actual = iter(self.for_node.children)

        for index, item in enumerate(new_items):
            for xml_node in xml_children:
                child = next(actual)

                assert child.xml_node == xml_node
                assert child.node_globals.to_dictionary() == {'index': index, 'item': item,
                                                              **self.for_node.node_globals.to_dictionary(),
                                                              'node': child}
                assert child.node_styles.to_dictionary() == self.for_node.node_styles.to_dictionary()
