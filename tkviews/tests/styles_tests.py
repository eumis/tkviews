from itertools import chain
from unittest.mock import Mock

from pytest import mark, raises
from pyviews.core.rendering import Node, NodeGlobals
from pyviews.core.xml import XmlAttr
from pyviews.pipes import call_set_attr

from tkviews.core import TkRenderingContext
from tkviews.styles import (STYLES_KEY, Style, StyleError, StylesView, apply_parent_items, apply_style_items,
                            apply_styles, setup_node_styles, store_to_globals, store_to_node_styles)


def some_setter():
    """Some test setter"""


def another_setter():
    """Another test setter"""


class SetupNodeStylesTest:
    """setup_node_styles tests"""

    @staticmethod
    def test_creates_node_styles():
        """should add node_styles to parent globals"""
        parent_node: Node = Mock(node_globals = NodeGlobals())

        setup_node_styles(Mock(), TkRenderingContext({'parent_node': parent_node}))
        actual = parent_node.node_globals.get(STYLES_KEY)

        assert isinstance(actual, NodeGlobals)

    @staticmethod
    def test_does_not_create_if_exist():
        """should not change parent node_globals if node_styles exist"""
        node_styles = NodeGlobals()
        parent_node: Node = Mock(node_globals = NodeGlobals({STYLES_KEY: node_styles}))

        setup_node_styles(Mock(), TkRenderingContext({'parent_node': parent_node}))
        actual = parent_node.node_globals[STYLES_KEY]

        assert node_styles == actual


class ApplyStyleItemsTests:
    """apply_style_items tests"""

    @staticmethod
    @mark.parametrize('attrs, expected', [
        ([('one', '{1}', None)], [('one', 1, call_set_attr)]),
        ([('one', ' value ', None)], [('one', ' value ', call_set_attr)]),
        ([('one', 'value', __name__ + '.some_setter')], [('one', 'value', some_setter)]),
        ([('one', 'value', __name__ + '.some_setter'),
          ('two', '{1 + 1}', None),
          ('key', '', __name__ + '.another_setter')],
         [('one', 'value', some_setter),
          ('two', 2, call_set_attr),
          ('key', '', another_setter)]),
        ([('one', 'value', __name__ + '.some_setter'),
          ('one', '', __name__ + '.another_setter')],
         [('one', 'value', some_setter),
          ('one', '', another_setter)])
     ]) # yapf: disable
    def test_creates_style_items_from_attrs(attrs, expected):
        """apply_style_items should create style item for every attribute"""
        attrs = [XmlAttr('name', 'hoho')] + [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
        xml_node = Mock(attrs = attrs)
        node = Style(xml_node)

        apply_style_items(node, TkRenderingContext())
        actual = [(item.name, item.value, item.setter) for name, item in node.items.items()]

        assert actual == expected

    @staticmethod
    def test_requires_name_attribute():
        """apply_style_items should raise StyleError if name attribute is missing"""
        xml_node = Mock(attrs = [])
        node = Style(xml_node)

        with raises(StyleError):
            apply_style_items(node, TkRenderingContext())

    @staticmethod
    @mark.parametrize('name', [
        '',
        'name',
        'some name',
        ' some name    ',
    ]) # yapf: disable
    def test_sets_style_name(name):
        """apply_style_items should set style name from attributes"""
        xml_node = Mock(attrs = [XmlAttr('name', name)])
        node = Style(xml_node)

        apply_style_items(node, TkRenderingContext())

        assert node.name == name


class ApplyParentItemsTests:
    """apply_parent_items tests"""

    @mark.parametrize('items, parent_items, expected', [
        ([('one', '{1}', None)], [], [('one', 1, call_set_attr)]),
        ([('one', ' value ', None)], [], [('one', ' value ', call_set_attr)]),
        ([('one', 'value', __name__ + '.some_setter')], [], [('one', 'value', some_setter)]),
        ([('one', 'value', __name__ + '.some_setter'),
          ('two', '{1 + 1}', None),
          ('key', '', __name__ + '.another_setter')],
         [],
         [('one', 'value', some_setter),
          ('two', 2, call_set_attr),
          ('key', '', another_setter)]),
        ([('one', 'value', __name__ + '.some_setter'),
          ('one', '', __name__ + '.another_setter')],
         [],
         [('one', 'value', some_setter),
          ('one', '', another_setter)])
    ]) # yapf: disable
    def test_uses_parent_style_items(self, items, parent_items, expected):
        """apply_parent_items should add parent style items"""
        node = self._get_style_node(items)
        parent_node = self._get_style_node(parent_items)

        apply_parent_items(node, TkRenderingContext({'parent_node': parent_node}))
        actual = [(item.name, item.value, item.setter) for name, item in node.items.items()]

        assert actual == expected

    @staticmethod
    def _get_style_node(attrs):
        attrs = [XmlAttr('name', 'hoho')] + [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
        xml_node = Mock(attrs = attrs)
        node = Style(xml_node)
        apply_style_items(node, TkRenderingContext())
        return node

    @staticmethod
    @mark.parametrize('parent_node', [None, Node(Mock())])
    def test_skips_not_style_parent(parent_node):
        """apply_parent_items do nothing if parent is not Style"""
        items = {'item': ('item', 'value')}
        node = Style(Mock())
        node.items = items.copy()

        apply_parent_items(node, TkRenderingContext({'parent_node': parent_node}))

        assert items == node.items


def test_store_to_node_styles():
    """store_to_node_styles should store style items to node_styles"""
    node_styles = NodeGlobals()
    node = Style(Mock())
    node.items = Mock()
    parent_node = Mock(node_globals = NodeGlobals({STYLES_KEY: node_styles}))

    store_to_node_styles(node, TkRenderingContext({'parent_node': parent_node}))

    assert node_styles[node.name] == node.items.values()


@mark.parametrize('parent_styles, view_styles, expected', [
    (None, {}, {}),
    ({}, {}, {}),
    (None, {'key': 'style'}, {'key': 'style'}),
    ({}, {'key': 'style'}, {'key': 'style'}),
    ({'key': 'style'}, {'style': 'style'}, {'key': 'style', 'style': 'style'}),
    ({'key': 'parent style'}, {'key': 'view style'}, {'key': 'view style'})
]) # yapf: disable
def test_store_to_globals(parent_styles, view_styles, expected):
    """should copy node styles from view root to parent globals"""
    parent_node = Mock(node_globals = NodeGlobals())
    if parent_styles:
        parent_node.node_globals[STYLES_KEY] = NodeGlobals(parent_styles)
    node = StylesView(Mock(), Mock())
    child = Mock(node_globals = NodeGlobals())
    child.node_globals[STYLES_KEY] = NodeGlobals(view_styles)
    node.add_child(child)

    store_to_globals(node, TkRenderingContext({'parent_node': parent_node}))
    actual = parent_node.node_globals[STYLES_KEY]

    assert expected == actual


class StyleTests:
    """style tests"""

    @staticmethod
    @mark.parametrize('style_keys, expected_keys', [
        ('one, two', ['one', 'two']),
        ('two, one', ['one', 'two']),
        ('one', ['one']),
        ('', []),
        (['one', 'two'], ['one', 'two']),
        (['two', 'one'], ['one', 'two']),
        (['one'], ['one']),
        ([''], ['']),
        ([], []),
    ]) # yapf: disable
    def test_applies_style_items(style_keys, expected_keys):
        """should apply style items"""
        node = Mock(node_globals = NodeGlobals())
        node_styles = {key: [Mock(apply = Mock())] for key in expected_keys}
        node.node_globals[STYLES_KEY] = NodeGlobals(node_styles)

        apply_styles(node, '', style_keys)
        called = True
        for item in chain(*node_styles.values()):
            called = item.apply.called and called

        assert called

    @staticmethod
    def test_raises_style_error():
        """should raise StyleError if style is not found"""
        node = Mock(node_globals = NodeGlobals())
        node.node_globals[STYLES_KEY] = NodeGlobals()

        with raises(StyleError):
            apply_styles(node, '', ['key'])
