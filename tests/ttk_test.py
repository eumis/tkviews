from unittest import TestCase, main
from unittest.mock import call, Mock
from pyviews.testing import case
from tkviews import ttk

class StyleTest(TestCase):
    @case('name', 'parent_name', 'name.parent_name')
    @case('name', None, 'name')
    @case('name', '', 'name')
    @case('name', ' ', 'name. ')
    def test_full_name(self, name, parent_name, expected):
        style = ttk.Style(None, parent_name=parent_name)

        style.name = name

        msg = 'full name should consists from'
        self.assertEqual(expected, style.full_name, msg=msg)

    @case('name', 'parent_name')
    @case('name', None)
    @case('name', '')
    @case('name', ' ')
    def test_get_node_args_adds_fullname(self, name, parent_name):
        style = ttk.Style(None, parent_name=parent_name)
        style.name = name

        args = style.get_node_args(None)

        msg = 'get_node_args should return args with parent_name key'
        self.assertEqual(style.full_name, args['parent_name'], msg=msg)

class ApplyTest(TestCase):
    def setUp(self):
        self._mocked_ttk_style = ttk.TtkStyle
        self._ttk_style = Mock()
        ttk.TtkStyle = Mock(return_value=self._ttk_style)

    @case({'name': 'name', 'key': 'value'}, {'key': 'value'})
    @case({'name': 'name', 'key': 'value', 'another_key': 'value'}, \
          {'key': 'value', 'another_key': 'value'})
    def test_apply(self, attrs, values):
        node = ttk.Style(None)

        for key, value in attrs.items():
            node.set_attr(key, value)

        node.apply()

        msg = 'name property should be set to node with set_attrs'
        self.assertEqual(attrs['name'], node.name, msg)

        msg = 'attr values should be applied to ttk.Style'
        values = {key: value for key, value in values.items() if key != 'name'}
        config_call = call(node.full_name, **values)
        self.assertEqual(self._ttk_style.configure.call_args, config_call, msg)

    @case(None)
    @case('')
    def test_apply_raises(self, name):
        node = ttk.Style(None)
        node.name = name

        msg = '"name" attribute value should be used as style name'
        with self.assertRaises(KeyError, msg=msg):
            node.apply()

    def tearDown(self):
        ttk.TtkStyle = self._mocked_ttk_style

class ModifiersTest(TestCase):
    def setUp(self):
        self._mocked_ttk_style = ttk.TtkStyle
        self._ttk_style = Mock()
        ttk.TtkStyle = Mock(return_value=self._ttk_style)

    def test_theme_use(self):
        theme = 'default'
        ttk.theme_use(None, theme, None)

        msg = 'theme_use should call theme_use for ttk.Style'
        self.assertEqual(self._ttk_style.theme_use.call_args, call(theme), msg)

    def test_apply(self):
        node = Mock()

        ttk.apply_ttk_style(node)

        msg = 'ttk.apply_ttk_style should call apply for passed node'
        self.assertTrue(node.apply.called, msg)

    def tearDown(self):
        ttk.TtkStyle = self._mocked_ttk_style

if __name__ == '__main__':
    main()
