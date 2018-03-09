from unittest import TestCase, main
from unittest.mock import call, Mock
from pyviews.testing import case
from tests.mock import some_modifier
from pyviews.core.ioc import Scope, scope, register_single
from pyviews.core.xml import XmlAttr, XmlNode
from pyviews.core.observable import InheritedDict
from tkviews.styles import StyleItem, Style, apply_attributes, apply_styles
from tkviews.modifiers import set_attr

class StyleItemTest(TestCase):
    @case('key', 1)
    @case('asdf', None)
    @case('', None)
    @case('', 1)
    def test_apply_should_call_modifier(self, name, value):
        modifier = Mock()
        item = StyleItem(modifier, name, value)
        node = Mock()

        item.apply(node)

        msg = 'apply should call passed modifier with parameters'
        self.assertEqual(modifier.call_args, call(node, name, value), msg)

def one_m():
    pass

def two_m():
    pass

class StyleTest(TestCase):
    def setUp(self):
        self.styles = {}
        with Scope('StyleTest'):
            register_single('styles', self.styles)
        self.style = Style(None)

    @scope('StyleTest')
    @case('name', [])
    @case('other_name', [StyleItem(None, None, None)])
    def test_set_items_should_set_to_styles_by_name(self, name, items):
        self.style.name = name
        self.style.set_items(items)

        msg = 'set_items should add passed items to context'
        self.assertEqual(items, self.styles[name], msg)

    @scope('StyleTest')
    @case([StyleItem(one_m, 'key', 'value')], [StyleItem(one_m, 'key', 'another_value')], \
          [StyleItem(one_m, 'key', 'another_value')])
    @case([StyleItem(one_m, 'key', 'value')], [StyleItem(two_m, 'key', 'another_value')], \
          [StyleItem(one_m, 'key', 'value'), StyleItem(two_m, 'key', 'another_value')])
    def test_set_items_gets_parent_styles(self, parent_styles, child_styles, expected):
        parent_name = 'parent'
        name = 'name'
        self.styles[parent_name] = parent_styles
        style = Style(None, parent_style=parent_name)
        style.name = name

        style.set_items(child_styles)

        msg = 'actual style_items are not equal to expected'
        self.assertTrue(_style_items_equal(expected, self.styles[name]), msg)

    @scope('StyleTest')
    @case('')
    @case(None)
    def test_set_items_should_raise_if_name_is_not_set(self, name):
        self.style.name = name

        msg = 'set_items should raise error if name is not set'
        with self.assertRaises(Exception, msg=msg):
            self.style.set_items([])

    @scope('StyleTest')
    def test_destroy_should_remove_styles_from_context(self):
        self.style.name = 'name'
        self.style.set_items([])

        self.style.destroy()

        msg = 'destroy should remove items from context'
        self.assertFalse(self.style.name in self.styles, msg)

def _style_items_equal(expected, actual):
    if len(expected) != len(actual):
        return False

    for i, item in enumerate(expected):
        result_item = actual[i]
        if item._modifier != result_item._modifier \
            or item._name != result_item._name \
            or item._value != result_item._value:
            return False

    return True

class ParsingTest(TestCase):
    def setUp(self):
        self.styles = {}
        with Scope('ParsingTest'):
            register_single('styles', self.styles)
            register_single('set_attr', set_attr)

    @scope('ParsingTest')
    @case([('name', 'some_style', None),
           ('key', 'value', None),
           ('key', 'other_value', 'tests.mock.some_modifier'),
           ('num', '{1}', None),
           ('num', '{count}', None),
           ('bg', '#000', None)],
          [StyleItem(set_attr, 'key', 'value'),
           StyleItem(some_modifier, 'key', 'other_value'),
           StyleItem(set_attr, 'num', 1),
           StyleItem(set_attr, 'num', 2),
           StyleItem(set_attr, 'bg', '#000')],
          {'count': 2})
    def test_apply_attributes_creates_style_items(self, attrs, style_items, global_values):
        xml_node = XmlNode('tkviews', 'StyleItem')
        xml_node.attrs = [XmlAttr(attr[0], attr[1], attr[2]) for attr in attrs]
        parent_globals = InheritedDict()
        for key, value in global_values.items():
            parent_globals[key] = value
        context = {'globals': parent_globals}
        style = Style(xml_node, context)

        apply_attributes(style)

        msg = 'actual style_items are not equal to expected'
        self.assertTrue(_style_items_equal(style_items, self.styles[style.name]), msg)

    @scope('ParsingTest')
    @case('name')
    @case('some name')
    def test_apply_attributes_sets_style_name(self, name):
        xml_node = XmlNode('nsp', 'node')
        xml_node.attrs = [XmlAttr('name', name)]
        style = Style(xml_node)

        apply_attributes(style)

        msg = '"name" attribute value should be used as style name'
        self.assertEqual(name, style.name, msg)

    @scope('ParsingTest')
    @case([('bg', '#000')])
    @case([('name', ''), ('bg', '#000')])
    @case([('name', None), ('bg', '#000')])
    def test_apply_attributes_raise_if_name_empty_or_not_exist(self, attrs):
        xml_node = XmlNode('nsp', 'node')
        xml_node.attrs = [XmlAttr(attr[0], attr[1]) for attr in attrs]
        style = Style(xml_node)

        msg = '"name" attribute value should be used as style name'
        with self.assertRaises(KeyError, msg=msg):
            apply_attributes(style)

class ApplyTest(TestCase):
    @case('one,two', ['one', 'two'], ['one', 'two', 'three'])
    @case('one , two', ['one', 'two'], ['one', 'two', 'three'])
    @case(['one', 'two'], ['one', 'two'], ['one', 'two', 'three'])
    def test_apply_styles(self, styles_to_apply, styles_applied, all_styles):
        styles = {}
        register_single('styles', styles)
        for key in all_styles:
            styles[key] = [Mock() for i in range(0, 5)]
        node = Mock()

        apply_styles(node, styles_to_apply)

        msg = 'style items should be applied to node from passed styles'
        self.assertTrue(self._styles_applied(node, styles, styles_applied), msg)

    def _styles_applied(self, node, styles, keys):
        for key, style_items in styles.items():
            for item in style_items:
                if key in keys and item.apply.call_args != call(node):
                    return False
                if key not in keys and item.apply.called:
                    return False

        return True

    def tearDown(self):
        register_single('styles', {})

if __name__ == '__main__':
    main()
