from unittest.mock import call, Mock, patch

from pytest import mark

from tkviews.node import ttk
from tkviews.node.ttk import TtkStyle, theme_use


class TtkStyleTests:
    @mark.parametrize('name, parent_name, expected', [
        ('name', 'parent_name', 'name.parent_name'),
        ('name', None, 'name'),
        ('name', '', 'name'),
        ('name', ' ', 'name. ')
    ])
    def test_full_name(self, name, parent_name, expected):
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
