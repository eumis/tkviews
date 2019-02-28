#pylint: disable=missing-docstring

from unittest import TestCase
from unittest.mock import call, Mock, patch
from pyviews.testing import case
from . import ttk
from .ttk import TtkStyle, theme_use

class TtkStyleTests(TestCase):
    @case('name', 'parent_name', 'name.parent_name')
    @case('name', None, 'name')
    @case('name', '', 'name')
    @case('name', ' ', 'name. ')
    def test_full_name(self, name, parent_name, expected):
        style = TtkStyle(None, parent_name=parent_name)

        style.name = name

        msg = 'full name should be in format "parent_name.name"'
        self.assertEqual(expected, style.full_name, msg=msg)

class ModifiersTest(TestCase):
    @patch(ttk.__name__ + '.Style')
    @case('default')
    @case('custom')
    def test_theme_use(self, ttk_style: Mock, theme):
        ttk_style_mock = Mock(theme_use=Mock())
        ttk_style.return_value = ttk_style_mock

        theme_use(Mock(), theme, '')

        msg = 'theme_use should call theme_use for ttk.Style'
        self.assertEqual(ttk_style_mock.theme_use.call_args, call(theme), msg)
