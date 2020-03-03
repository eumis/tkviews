from unittest.mock import Mock, call

from pytest import mark, raises, fixture
from pyviews.core import XmlAttr, InheritedDict, Node
from pyviews.pipes import call_set_attr

from tkviews import WidgetNode
from tkviews.core.rendering import TkRenderingContext
from tkviews.styles import Style, StyleError, StyleItem, apply_styles
from tkviews.styles import apply_style_items, apply_parent_items, store_to_node_styles


def some_setter():
    """Some test setter"""


def another_setter():
    """Another test setter"""


class StyleItemTests:
    @staticmethod
    def test_apply():
        """should call passed setter with parameters"""
        setter, name, value = Mock(), 'name', 'value'
        item, node = StyleItem(setter, name, value), Node(Mock())

        item.apply(node)

        assert setter.call_args == call(node, name, value)

    @staticmethod
    @mark.parametrize('one, two, equal', [
        (StyleItem(some_setter, 'name', 1), StyleItem(some_setter, 'name', 1), True),
        (StyleItem(some_setter, 'name', 'value'),
         StyleItem(some_setter, 'name', 'other value'), True),
        (StyleItem(some_setter, 'name', 1), StyleItem(some_setter, 'other name', 1), False),
        (StyleItem(some_setter, 'name', 1), StyleItem(another_setter, 'name', 1), False)
    ])
    def test_eq(one, two, equal):
        """should compare by name and setter"""
        actual = one == two

        assert actual == equal


@mark.usefixtures('container_fixture')
class ApplyStyleItemsTests:
    """apply_style_items() tests"""

    @staticmethod
    @mark.parametrize('attrs, expected', [
        ([('one', '1', None)], [('one', '1', call_set_attr)]),
        ([('one', '{1}', None)], [('one', 1, call_set_attr)]),
        ([('one', ' value ', None)], [('one', ' value ', call_set_attr)]),
        ([('one', 'value', __name__ + '.some_setter')], [('one', 'value', some_setter)]),
        ([('one', 'value', __name__ + '.some_setter'),
          ('two', '{1 + 1}', None),
          ('key', '', __name__ + '.another_setter')
          ],
         [('one', 'value', some_setter),
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

        apply_style_items(node, TkRenderingContext())
        actual = {name: (item.name, item.value, item.setter) for name, item in node.items.items()}
        expected = {item[0]: item for item in expected}

        assert actual == expected

    @staticmethod
    def test_requires_name_attribute():
        """should raise StyleError if name attribute is missing"""
        xml_node = Mock(attrs=[])
        node = Style(xml_node)

        with raises(StyleError):
            apply_style_items(node, TkRenderingContext())

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

        apply_style_items(node, TkRenderingContext())

        assert node.name == name


@mark.parametrize('items, parent_items, expected', [
    ([('one', 'value'), ('key', '')],
     [('one', 'parent value'), ('two', 2)],
     [('one', 'value'), ('key', ''), ('two', 2)]
     ),
    ([],
     [('one', 'value'), ('two', 2)],
     [('one', 'value'), ('two', 2)]
     ),
    ([('one', 'value'), ('two', 2)],
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

    apply_parent_items(node, TkRenderingContext({
        'parent_name': 'parent',
        'node_styles': node_styles
    }))

    assert node.items == expected


def test_store_to_node_styles():
    """should store style items to node_styles"""
    node_styles = InheritedDict()
    node = Style(Mock())
    node.items = Mock()

    store_to_node_styles(node, TkRenderingContext({'node_styles': node_styles}))

    assert node_styles[node.name] == node.items.values()


@fixture
def apply_styles_fixture(request):
    request.cls.node = WidgetNode(Mock(), Mock(), node_styles=InheritedDict({
        'one': [Mock(), Mock()],
        'two': [Mock(), Mock(), Mock()],
        'three': [Mock()]
    }))


@mark.usefixtures('apply_styles_fixture')
class ApplyStylesTests:
    """apply_styles() setter tests"""

    @mark.parametrize('styles, keys', [
        ('', []),
        (None, []),
        ('one', ['one']),
        ('one', ['one']),
        ('one,two', ['one', 'two']),
        ('one,two,three', ['one', 'two', 'three']),
        ([], []),
        (['one'], ['one']),
        (['one', 'two'], ['one', 'two'])
    ])
    def test_applies_styles(self, styles, keys):
        """Parses input and applies styles"""
        apply_styles(self.node, '', styles)
        node_styles = self.node.node_styles.to_dictionary()
        actual = {key for key, items in node_styles.items() if
                  all([i.apply.called for i in items])}

        assert actual == set(keys)

    @mark.parametrize('styles', ['four', 'one, four'])
    def test_raises_for_unknown_key(self, styles):
        """should raise StyleError for unknown style"""
        with raises(StyleError):
            apply_styles(self.node, '', styles)
