from unittest.mock import Mock, call

from pytest import mark
from pyviews.core import XmlNode, Node
from tkviews.node.containers import View, For, If


class ViewTests:
    """View node tests"""

    @staticmethod
    def test_init():
        """__init__() should sent name to None"""
        view = View(Mock(), Mock())

        assert view.name is None

    @staticmethod
    @mark.parametrize('old_name, new_name', [
        (None, 'name'),
        ('name', 'another name')
    ])
    def test_name_changed(old_name, new_name):
        """name_changed() should be called on name change"""
        view = View(Mock(), Mock())
        view.name = old_name
        view.name_changed = Mock()

        view.name = new_name

        assert view.name_changed.call_args == call(view, new_name, old_name)

    @staticmethod
    @mark.parametrize('content_root', [
        (Node(XmlNode('', '')))
    ])
    def test_set_content(content_root: Node):
        """should set content as children nodes"""
        view = View(Mock(), Mock())

        view.set_content(content_root)

        assert view.children == [content_root]


class ForTests:
    """For node tests"""

    @staticmethod
    def test_init():
        """condition should be False by default"""
        node = If(Mock(), Mock())

        assert not node.condition

    @staticmethod
    @mark.parametrize('old_items, new_items', [
        ([], [Mock()]),
        ([Mock()], []),
        ([Mock()], [Mock(), Mock()])
    ])
    def test_called_on_items_changed(old_items, new_items):
        """items_changed() should be called on items change"""
        node = For(Mock(), Mock())
        node.items = old_items
        node.items_changed = Mock()

        node.items = new_items

        assert node.items_changed.call_args == call(node, new_items, old_items)


class IfTests:
    """If node tests"""

    @staticmethod
    @mark.parametrize('old_condition, new_condition', [
        (False, True),
        (True, False)
    ])
    def test_condition_changed_called(old_condition, new_condition):
        """condition_changed should be called on condition change"""
        node = If(Mock(), Mock())
        node.condition = old_condition
        node.condition_changed = Mock()

        node.condition = new_condition

        assert node.condition_changed.call_args == call(node, new_condition, old_condition)
