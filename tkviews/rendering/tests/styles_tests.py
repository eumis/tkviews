from unittest.mock import Mock

from injectool import make_default, add_resolve_function
from pytest import mark, raises
from pyviews.core import XmlAttr, InheritedDict, Expression
from pyviews.compilation import CompiledExpression
from pyviews.rendering import call_set_attr
from tkviews.node import Style, StyleError
from tkviews.rendering.styles import apply_style_items, apply_parent_items, store_to_node_styles

with make_default('styles_tests'):
    add_resolve_function(Expression, lambda c, p: CompiledExpression(p))


def some_setter():
    """Some test setter"""


def another_setter():
    """Another test setter"""


class ApplyStyleItemsTests:
    """apply_style_items() tests"""

    @staticmethod
    @mark.parametrize('attrs, expected', [
        ([('one', '1', None)], [('one', '1', call_set_attr)]),
        ([('one', '{1}', None)], [('one', 1, call_set_attr)]),
        ([('one', ' value ', None)], [('one', ' value ', call_set_attr)]),
        ([('one', 'value', __name__ + '.some_setter')], [('one', 'value', some_setter)]),
        (
                [
                    ('one', 'value', __name__ + '.some_setter'),
                    ('two', '{1 + 1}', None),
                    ('key', '', __name__ + '.another_setter')
                ],
                [
                    ('one', 'value', some_setter),
                    ('two', 2, call_set_attr),
                    ('key', '', another_setter)
                ]
        )
    ])
    def test_creates_style_items_from_attrs(attrs, expected):
        """should create style item for every attribute"""
        attrs = [XmlAttr('name', 'hoho')] + [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
        xml_node = Mock(attrs=attrs)
        node = Style(xml_node)

        with make_default('styles_tests'):
            apply_style_items(node)
        actual = {name: (item.name, item.value, item.setter) for name, item in node.items.items()}
        expected = {item[0]: item for item in expected}

        assert actual == expected

    @staticmethod
    def test_requires_name_attribute():
        """should raise StyleError if name attribute is missing"""
        xml_node = Mock(attrs=[])
        node = Style(xml_node)

        with raises(StyleError):
            apply_style_items(node)

    @staticmethod
    @mark.parametrize('name', [
        ''
        'name'
        'some name'
        ' some name    '
    ])
    def test_sets_style_name(name):
        """should set style name from attributes"""
        xml_node = Mock(attrs=[XmlAttr('name', name)])
        node = Style(xml_node)

        with make_default('styles_tests'):
            apply_style_items(node)

        assert node.name == name


@mark.parametrize('items, parent_items, expected', [
    (
            [('one', 'value'), ('key', '')],
            [('one', 'parent value'), ('two', 2)],
            [('one', 'value'), ('key', ''), ('two', 2)]
    ),
    (
            [],
            [('one', 'value'), ('two', 2)],
            [('one', 'value'), ('two', 2)]
    ),
    (
            [('one', 'value'), ('two', 2)],
            [],
            [('one', 'value'), ('two', 2)]
    )
])
def test_apply_parent_items_(items, parent_items, expected):
    """should add parent style items"""
    node = Style(Mock())
    node.items = {item[0]: item for item in items}
    node_styles = InheritedDict({'parent': {item[0]: item for item in parent_items}})
    expected = {item[0]: item for item in expected}

    apply_parent_items(node, parent_name='parent', node_styles=node_styles)

    assert node.items == expected


def test_store_to_node_styles():
    """should store style items to node_styles"""
    node_styles = InheritedDict()
    node = Style(Mock())
    node.items = Mock()

    store_to_node_styles(node, node_styles=node_styles)

    assert node_styles[node.name] == node.items.values()
