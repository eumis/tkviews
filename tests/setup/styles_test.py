from unittest import TestCase, main
from unittest.mock import call, Mock
from pyviews.testing import case
from pyviews.core.xml import XmlAttr, XmlNode
from pyviews.core.observable import InheritedDict
from pyviews.rendering.flow import get_setter, default_setter
from tkviews.core.styles import Style, StyleItem
from tkviews.setup.styles import apply_style_items, StyleError
from tkviews.setup.styles import apply_parent_items, store_to_node_styles

def some_setter():
    '''Some test setter'''
    pass

def another_setter():
    '''Another test setter'''
    pass

from tests.setup.styles_test import some_setter, another_setter

class ApplyStyleItemsTests(TestCase):
    @case([('one', '1', None)], [('one', '1', default_setter)])
    @case([('one', '{1}', None)], [('one', 1, default_setter)])
    @case([('one', ' value ', None)], [('one', ' value ', default_setter)])
    @case([('one', 'value', 'tests.setup.styles_test.some_setter')], [('one', 'value', some_setter)])
    @case(
        [
            ('one', 'value', 'tests.setup.styles_test.some_setter'),
            ('two', '{1 + 1}', None),
            ('key', '', 'tests.setup.styles_test.another_setter')
        ],
        [
            ('one', 'value', some_setter),
            ('two', 2, default_setter),
            ('key', '', another_setter)
        ]
    )
    def test_apply_style_items_creates_style_items_from_attrs(self, attrs, expected):
        attrs = [XmlAttr('name', 'hoho')] + [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
        xml_node = Mock(attrs=attrs)
        node = Style(xml_node)

        apply_style_items(node)
        actual = {name: (item.name, item.value, item.setter) for name, item in node.items.items()}
        expected = {item[0]: item for item in expected}

        msg = 'apply_style_items should create style item for every attribute'
        self.assertDictEqual(actual, expected, msg)

    def test_apply_style_items_requires_name_attribute(self):
        xml_node = Mock(attrs=[])
        node = Style(xml_node)

        msg = 'apply_style_items should raise StyleError if name attribute is missing'
        with self.assertRaises(StyleError, msg=msg):
            apply_style_items(node)

    @case('')
    @case('name')
    @case('some name')
    @case(' some name    ')
    def test_apply_style_items_sets_style_name(self, name):
        xml_node = Mock(attrs=[XmlAttr('name', name)])
        node = Style(xml_node)

        apply_style_items(node)

        msg = 'apply_style_items should set style name from attributes'
        self.assertEqual(node.name, name, msg)

class ApplyParentItemsTets(TestCase):
    @case(
        [('one', 'value'), ('key', '')],
        [('one', 'parent value'), ('two', 2)],
        [('one', 'value'), ('key', ''), ('two', 2)]
    )
    @case(
        [],
        [('one', 'value'), ('two', 2)],
        [('one', 'value'), ('two', 2)]
    )
    @case(
        [('one', 'value'), ('two', 2)],
        [],
        [('one', 'value'), ('two', 2)]
    )
    def test_apply_parent_items_(self, items, parent_items, expected):
        node = Style(Mock())
        node.items = {item[0]: item for item in items}
        node_styles = InheritedDict({'parent': {item[0]: item for item in parent_items}})
        expected = {item[0]: item for item in expected}

        apply_parent_items(node, parent_name='parent', node_styles=node_styles)

        msg = 'apply_parent_items should add parent style items'
        self.assertDictEqual(node.items, expected, msg)

class StoreToNodeStylesTests(TestCase):
    def test_store_to_node_styles(self):
        node_styles = InheritedDict()
        node = Style(Mock())
        node.items = Mock()

        store_to_node_styles(node, node_styles=node_styles)

        msg = 'store_to_node_styles should store style items to node_styles'
        self.assertEqual(node_styles[node.name], node.items, msg)

if __name__ == '__main__':
    main()
