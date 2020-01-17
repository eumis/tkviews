from unittest.mock import call, Mock, patch

from pytest import mark
from pyviews.core import XmlAttr
from pyviews.pipes import call_set_attr

from tkviews import ttk
from tkviews.core.common import TkRenderingContext
from tkviews.ttk import TtkStyle, theme_use, setup_value_setter, configure, apply_style_attributes


class TtkStyleTests:
    @staticmethod
    @mark.parametrize('name, parent_name, expected', [
        ('name', 'parent_name', 'name.parent_name'),
        ('name', None, 'name'),
        ('name', '', 'name'),
        ('name', ' ', 'name. ')
    ])
    def test_full_name(name, parent_name, expected):
        """full name should be in format "parent_name.name"""
        style = TtkStyle(None, parent_name=parent_name)

        style.name = name

        assert expected == style.full_name


@mark.parametrize('theme', [
    'default',
    'custom'
])
def test_theme_use(theme):
    """theme_use() should call theme_use for ttk.Style"""
    with patch(ttk.__name__ + '.Style') as ttk_style:
        ttk_style_mock = Mock(theme_use=Mock())
        ttk_style.return_value = ttk_style_mock

        theme_use(Mock(), theme, '')

        assert ttk_style_mock.theme_use.call_args == call(theme)


def increment(node, key, value):
    """Increments value"""
    call_set_attr(node, key, value + 1)


class SetupValueSetterTests:
    """setup_value_setter() tests"""

    @staticmethod
    def test_sets_name():
        """should set setter that sets node properties"""
        node = TtkStyle(Mock())
        name = 'some_name'

        setup_value_setter(node, TkRenderingContext())
        node.set_attr('name', name)

        assert node.name == name

    @staticmethod
    @mark.parametrize('values', [
        ({'key': 'value'}),
        ({'key': 'value', 'another_key': 1})
    ])
    def test_sets_values(values: dict):
        """should set setter that sets to "values" property"""
        node = TtkStyle(Mock())

        setup_value_setter(node, TkRenderingContext())
        for key, value in values.items():
            node.set_attr(key, value)

        assert node.values == values


@mark.parametrize('attrs, expected', [
    ([], {}),
    ([('one', '1', None)], {'one': '1'}),
    ([('one', '{1}', None)], {'one': 1}),
    ([('one', '{5}', __name__ + '.increment')], {'one': 6}),
    (
            [
                ('one', '{1 + 1}', None),
                ('two', '{1 + 1}', __name__ + '.increment'),
                ('key', ' string value ', None)
            ],
            {
                'one': 2,
                'two': 3,
                'key': ' string value '
            }
    )
])
def test_apply_style_attributes(attrs: list, expected: dict):
    """should set attribute values"""
    attrs = [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
    xml_node = Mock(attrs=attrs)
    node = TtkStyle(xml_node)
    setup_value_setter(node, TkRenderingContext())

    apply_style_attributes(node, TkRenderingContext())

    assert node.values == expected


@mark.parametrize('name, values', [
    ('name', {}),
    ('Button.Some', {'one': 1}),
    ('Label', {'one': 1, 'two': 'two'})
])
def test_configure_pass_values(name: str, values: dict):
    """configure should call configure on ttk style and pass values"""
    with patch(ttk.__name__ + '.Style') as ttk_style:
        configure_mock = Mock()
        ttk_style.return_value = Mock(configure=configure_mock)
        node = TtkStyle(Mock())
        node.values = values
        node.name = name

        configure(node, TkRenderingContext())

        assert configure_mock.call_args == call(node.full_name, **node.values)
