from unittest import TestCase, main
from unittest.mock import Mock, patch, call
from pyviews.testing import case
from pyviews.core.xml import XmlAttr
from pyviews.rendering.flow import default_setter
from tkviews.core.ttk import TtkStyle
from tkviews.setup.ttk import setup_value_setter, apply_style_attributes, configure

def increment(node, key, value):
    '''Increments value'''
    default_setter(node, key, value + 1)

from tests.setup.ttk_test import increment

class SetupTests(TestCase):
    def test_setup_value_setter_sets_name(self):
        node = TtkStyle(Mock())
        name = 'some_name'

        setup_value_setter(node)
        node.setter(node, 'name', name)

        msg = 'setup_value_setter should set setter that sets node properties'
        self.assertEqual(node.name, name, msg)

    @case({'key':'value'})
    @case({'key':'value', 'another_key':1})
    def test_setup_value_setter_sets_values(self, values: dict):
        node = TtkStyle(Mock())

        setup_value_setter(node)
        for key, value in values.items():
            node.setter(node, key, value)

        msg = 'setup_value_setter should set setter that sets to "values" property'
        self.assertDictEqual(node.values, values, msg)

    @case([], {})
    @case([('one', '1', None)], {'one': '1'})
    @case([('one', '{1}', None)], {'one': 1})
    @case([('one', '{5}', 'tests.setup.ttk_test.increment')], {'one': 6})
    @case(
        [
            ('one', '{1 + 1}', None),
            ('two', '{1 + 1}', 'tests.setup.ttk_test.increment'),
            ('key', ' string value ', None)
        ],
        {
            'one': 2,
            'two': 3,
            'key': ' string value '
        }
    )
    def test_apply_style_attributes_sets_values(self, attrs: list, expected: dict):
        attrs = [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
        xml_node = Mock(attrs=attrs)
        node = TtkStyle(xml_node)
        setup_value_setter(node)

        apply_style_attributes(node)

        msg = 'apply_style_attributes should set attribte values'
        self.assertDictEqual(node.values, expected, msg)

    @patch('tkviews.setup.ttk.Style')
    @case('name', {})
    @case('Button.Some', {'one': 1})
    @case('Label', {'one': 1, 'two': 'two'})
    def test_configure_pass_values(self, ttk_style: Mock, name: str, values: dict):
        ttk_style_mock = Mock(configure=Mock())
        ttk_style.return_value = ttk_style_mock
        node = TtkStyle(Mock())
        node.values = values
        node.name = name

        configure(node)

        msg = 'configure should call configure on ttk style and pass values'
        self.assertEqual(ttk_style_mock.configure.call_args, call(node.full_name, **values), msg)

if __name__ == '__main__':
    main()
