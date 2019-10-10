from unittest.mock import Mock, call

from pytest import mark

from tkviews.node import CanvasNode
from tkviews.rendering.canvas import setup_temp_setter, setup_temp_binding, create_item
from tkviews.rendering.canvas import setup_config_setter, apply_temp_events, setup_event_binding
from tkviews.rendering.canvas import clear_temp
from tkviews.rendering.common import TkRenderingContext


class TestCanvasNode(CanvasNode):
    def _create(self, **options):
        return "id"


class RenderStepsTests:
    @staticmethod
    @mark.parametrize('attrs', [
        {'key': 1},
        {'key': 1, 'one': 'one'},
        {'key': None, 'list': [1], 'obj': object()}
    ])
    def test_setup_temp_setter_stores_attributes(attrs: dict):
        """setup_temp_setter() should set setter that stores attrs it attr_values property"""
        canvas = TestCanvasNode(Mock(), Mock())

        setup_temp_setter(canvas, TkRenderingContext())

        for key, value in attrs.items():
            canvas.set_attr(key, value)
        assert canvas.attr_values == attrs

    @staticmethod
    @mark.parametrize('events', [
        {'key': lambda: None},
        {'key': lambda: None, 'two': lambda: None}
    ])
    def test_setup_temp_binding_stores_commands(events):
        """setup_temp_binding() should set bind that stores callbacks it events property"""
        canvas = TestCanvasNode(Mock(), Mock())

        setup_temp_binding(canvas, TkRenderingContext())

        for key, command in events.items():
            canvas.bind(key, command)
        assert canvas.events == events

    @staticmethod
    def test_create_item_calls_create():
        """create_item( should call create method of CanvasNode"""
        canvas = Mock()
        canvas.create = Mock()

        create_item(canvas, TkRenderingContext())

        assert canvas.create.called

    @staticmethod
    @mark.parametrize('key, value', [
        ('key', 1),
        ('other_key', 'value')
    ])
    def test_setup_config_setter_calls_config(key, value):
        """setup_config_setter() should set setter that calls config method"""
        canvas = TestCanvasNode(Mock(), Mock())
        canvas.config = Mock()

        setup_config_setter(canvas, TkRenderingContext())

        canvas.set_attr(key, value)
        assert canvas.config.call_args == call(**{key: value})

    @staticmethod
    def test_setup_event_binding_should_restore_bind():
        """setup_event_binding() should restore canvas bind method"""
        canvas = Mock()
        canvas.bind = Mock()

        setup_temp_binding(canvas, TkRenderingContext())
        setup_event_binding(canvas, TkRenderingContext())
        canvas.bind()

        assert canvas.bind.called

    @staticmethod
    @mark.parametrize('events', [
        {'key': lambda: None},
        {'key': lambda: None, 'two': lambda: None}
    ])
    def test_apply_temp_events_should_bind(events: dict):
        """apply_temp_events() should bind events stored in temp dictionary"""
        canvas = Mock()
        canvas.bind = Mock()
        canvas.events = events

        apply_temp_events(canvas, TkRenderingContext())

        expected_calls = [call(event, command) for event, command in events.items()]
        assert canvas.bind.call_args_list == expected_calls

    @staticmethod
    def test_clear_temp_deletes_temp_vars():
        """clear_temp() should delete temp properties"""
        canvas = TestCanvasNode(Mock(), Mock())
        canvas.attr_values = {}
        canvas.events = {}
        canvas.bind_source = {}

        clear_temp(canvas, TkRenderingContext())

        assert not hasattr(canvas, 'attr_values')
        assert not hasattr(canvas, 'events')
        assert not hasattr(canvas, 'bind_source')
