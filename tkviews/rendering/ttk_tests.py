#pylint: disable=missing-docstring

from unittest import TestCase
from unittest.mock import Mock, patch, call
from pyviews.testing import case
from pyviews.core.ioc import Scope, register_func
from pyviews.core.xml import XmlAttr
from pyviews.compilation import CompiledExpression
from pyviews.rendering import call_set_attr
from tkviews.node import TtkStyle
from . import ttk
from .ttk import setup_value_setter, apply_style_attributes, configure

with Scope('ttk_tests'):
    register_func('expression', CompiledExpression)

def increment(node, key, value):
    '''Increments value'''
    call_set_attr(node, key, value + 1)

class SetupTests(TestCase):
    def test_setup_value_setter_sets_name(self):
        node = TtkStyle(Mock())
        name = 'some_name'

        setup_value_setter(node)
        node.set_attr('name', name)

        msg = 'setup_value_setter should set setter that sets node properties'
        self.assertEqual(node.name, name, msg)

    @case({'key':'value'})
    @case({'key':'value', 'another_key':1})
    def test_setup_value_setter_sets_values(self, values: dict):
        node = TtkStyle(Mock())

        setup_value_setter(node)
        for key, value in values.items():
            node.set_attr(key, value)

        msg = 'setup_value_setter should set setter that sets to "values" property'
        self.assertDictEqual(node.values, values, msg)

    @case([], {})
    @case([('one', '1', None)], {'one': '1'})
    @case([('one', '{1}', None)], {'one': 1})
    @case([('one', '{5}', __name__ + '.increment')], {'one': 6})
    @case(
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
    def test_apply_style_attributes_sets_values(self, attrs: list, expected: dict):
        attrs = [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
        xml_node = Mock(attrs=attrs)
        node = TtkStyle(xml_node)
        setup_value_setter(node)

        with Scope('ttk_tests'):
            apply_style_attributes(node)

        msg = 'apply_style_attributes should set attribte values'
        self.assertDictEqual(node.values, expected, msg)

    @patch(ttk.__name__ + '.Style')
    @case('name', {})
    @case('Button.Some', {'one': 1})
    @case('Label', {'one': 1, 'two': 'two'})
    def test_configure_pass_values(self, ttk_style: Mock, name: str, values: dict):
        configure_mock = Mock()
        ttk_style.return_value = Mock(configure=configure_mock)
        node = TtkStyle(Mock())
        node.values = values
        node.name = name

        configure(node)

        msg = 'configure should call configure on ttk style and pass values'
        self.assertEqual(configure_mock.call_args, call(node.full_name, **node.values), msg)
