from tkinter import Listbox
from unittest.mock import Mock, call

from pytest import mark, fixture, raises
from pyviews.rendering import RenderingError

from tkviews import ListboxItem
from tkviews.core import TkRenderingContext
from tkviews.listbox import insert_item, setup_on_updated


class TestListbox(Listbox):
    def __init__(self):
        pass


@fixture
def listbox_fixture(request):
    request.cls.listbox_item = ListboxItem(Mock())
    listbox = TestListbox()
    request.cls.listbox = listbox
    listbox.size = Mock()
    listbox.insert = Mock()
    listbox.delete = Mock()
    request.cls.context = TkRenderingContext({'master': listbox})


@mark.usefixtures('listbox_fixture')
class ListboxPipelineTests:
    def test_insert_item_checks_parent(self):
        """should raise if master is not Listbox"""
        with raises(RenderingError):
            insert_item(self.listbox_item, TkRenderingContext({'master': Mock()}))

    @mark.parametrize('index, value', [
        (0, 'one'),
        (1, 'two'),
        (5, 'three')
    ])
    def test_insert_item_add_item_to_end(self, index: int, value: str):
        """should insert item to listbox"""
        self.listbox.size.side_effect = lambda: index
        self.listbox_item.value = value

        insert_item(self.listbox_item, self.context)

        assert self.listbox.insert.call_args == call(index, value)

    @mark.parametrize('index, value', [
        (0, 'one'),
        (1, 'two'),
        (5, 'three')
    ])
    def test_setup_on_index_updated(self, index: int, value: str):
        """should update item"""
        self.listbox_item.value = value

        setup_on_updated(self.listbox_item, self.context)
        self.listbox_item.index = index

        assert self.listbox.delete.call_args == call(index)
        assert self.listbox.insert.call_args == call(index, value)

    @mark.parametrize('index, value', [
        (0, 'one'),
        (1, 'two'),
        (5, 'three')
    ])
    def test_setup_on_value_updated(self, index: int, value: str):
        """should update item"""
        self.listbox_item.index = index

        setup_on_updated(self.listbox_item, self.context)
        self.listbox_item.value = value

        assert self.listbox.delete.call_args == call(index)
        assert self.listbox.insert.call_args == call(index, value)
