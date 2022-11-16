from tkinter import Widget
from typing import cast
from unittest.mock import Mock, call, patch

from pytest import fixture, mark
from pyviews.rendering import RenderingPipeline

from tkviews.core import TkRenderingContext
from tkviews.widgets import node
from tkviews.widgets.node import WidgetNode, Root, get_widget_pipeline
from tkviews.widgets.node import setup_widget_setter, setup_widget_destroy, apply_text


@fixture
def root_fixture(request):
    with patch(node.__name__ + '.Tk') as tk_mock:
        tk_instance = Mock()
        tk_mock.side_effect = lambda: tk_instance

        request.cls.root = Root(Mock())
        request.cls.tk_instance = tk_instance

        yield tk_mock


@mark.usefixtures('root_fixture')
class RootTests:
    """WidgetNode tests"""

    root: Root
    tk_instance: Mock

    def test_creates_tk_instance(self):
        """should create tkinter.Tk instance"""
        assert self.root.instance == self.tk_instance

    def test_bind(self):
        """should call widget.bind"""
        event, command = 'Button-1', Mock()

        self.root.bind(event, command)

        assert self.root.instance.bind.call_args == call(event, command)

    def test_bind_all(self):
        """should call widget.bind_all"""
        event, command = 'Button-1', Mock()

        self.root.bind_all(event, command)

        assert self.root.instance.bind_all.call_args == call(event, command)

    def test_state_getter(self):
        """should return Tk.state() method result"""
        state = Mock()
        self.root.instance.state.side_effect = lambda: state

        actual = self.root.state

        assert actual == state

    def test_state_setter(self):
        """should call Tk.state() method"""
        state = Mock()

        self.root.state = state

        assert self.root.instance.state.call_args == call(state)

    def test_icon(self):
        """should set icon"""
        icon = Mock()

        self.root.icon = icon

        assert self.root.icon == icon
        assert self.root.instance.iconbitmap.call_args == call(default=icon)


class TestWidget:
    def __init__(self):
        self.node_key = None
        self.instance_key = None
        self.destroy = Mock()
        self.configure = Mock()


class TestNode(WidgetNode):
    def __init__(self, widget):
        super().__init__(widget, Mock())
        self.node_key = None


@fixture
def widget_node_fixture(request):
    request.cls.node = TestNode(Mock())


@mark.usefixtures('widget_node_fixture')
class WidgetNodeTests:
    """WidgetNode tests"""

    node: TestNode

    def test_bind(self):
        """should call widget.bind"""
        event, command = 'Button-1', Mock()

        self.node.bind(event, command)

        assert self.node.instance.bind.call_args == call(event, command)

    def test_bind_all(self):
        """should call widget.bind_all"""
        event, command = 'Button-1', Mock()

        self.node.bind_all(event, command)

        assert self.node.instance.bind_all.call_args == call(event, command)


def test_get_widget_setup():
    """should return rendering pipeline"""
    actual = get_widget_pipeline()

    assert actual is not None
    assert isinstance(actual, RenderingPipeline)


@fixture
def setter_fixture(request):
    inst = TestWidget()
    test_node = TestNode(cast(Widget, inst))
    setup_widget_setter(test_node, TkRenderingContext())

    request.cls.inst = inst
    request.cls.node = test_node


@mark.usefixtures('setter_fixture')
class SetupWidgetSetterTests:
    """setup_widget_setter() tests"""

    inst: TestWidget
    node: TestNode

    @mark.parametrize('value', [1, 'value'])
    def test_sets_node_key(self, value):
        """should set node attribute if it exists"""
        self.node.set_attr('node_key', value)

        assert self.node.node_key == value
        assert self.inst.node_key is None

    @mark.parametrize('value', [1, 'value'])
    def test_sets_instance_key(self, value):
        """should set widget attribute if it exists"""
        self.node.set_attr('instance_key', value)

        assert self.inst.instance_key == value

    @mark.parametrize('key, value', [('int_key', 1), ('str_key', 'value')])
    def test_calls_configure(self, key, value):
        """should call configure if none of widget and node contains attribute"""
        self.node.set_attr(key, value)

        assert self.inst.configure.call_args == call(**{key: value})


def test_setup_widget_destroy():
    """should call widget.destroy() on node destroy"""
    inst = TestWidget()
    test_node = TestNode(cast(Widget, inst))

    setup_widget_destroy(test_node, TkRenderingContext())
    test_node.destroy()

    assert inst.destroy.called


@fixture
def apply_text_fixture(request):
    test_node = TestNode(Mock(text=''))
    test_node.set_attr = Mock()

    request.cls.node = test_node


@mark.usefixtures('binder_fixture', 'apply_text_fixture', )
class ApplyTextTests:
    """apply_text() step tests"""

    node: TestNode

    @mark.parametrize('text', [None, '', '    '])
    def test_empty(self, text):
        """should return if text is empty"""
        self.node.xml_node.text = text

        apply_text(self.node, TkRenderingContext())

        assert not self.node.set_attr.called

    @mark.parametrize('text, value', [('some value', 'some value'), ('{1 + 1}', 2)])
    def test_calls_set_attr(self, text, value):
        """should set value as "text" attribute"""
        self.node.xml_node.text = text

        apply_text(self.node, TkRenderingContext())

        assert self.node.set_attr.call_args == call('text', value)
