#pylint: disable=missing-docstring

from unittest import TestCase
from unittest.mock import Mock, call
from pyviews.testing import case
from tkviews.node import CanvasNode
from .canvas import setup_temp_setter, setup_temp_binding, create_item
from .canvas import setup_config_setter, apply_temp_events, setup_event_binding
from .canvas import clear_temp

class TestCanvasNode(CanvasNode):
    def _create(self, **options):
        return "id"

class RenderStepsTest(TestCase):
    @case({'key': 1})
    @case({'key': 1, 'one': 'one'})
    @case({'key': None, 'list': [1], 'obj': object()})
    def test_setup_temp_setter_stores_attributes(self, attrs: dict):
        canvas = TestCanvasNode(Mock(), Mock())

        setup_temp_setter(canvas)
        for key, value in attrs.items():
            canvas.set_attr(key, value)

        msg = 'setup_temp_setter should set setter that stores attrs it attr_values property'
        self.assertDictEqual(canvas.attr_values, attrs, msg)

    @case({'key': lambda: None})
    @case({'key': lambda: None, 'two': lambda: None})
    def test_setup_temp_binding_stores_commands(self, events):
        canvas = TestCanvasNode(Mock(), Mock())

        setup_temp_binding(canvas)
        for key, command in events.items():
            canvas.bind(key, command)

        msg = 'setup_temp_binding should set bind that stores callbacks it events property'
        self.assertDictEqual(canvas.events, events, msg)

    def test_create_item_calls_create(self):
        canvas = Mock()
        canvas.create = Mock()

        create_item(canvas)

        msg = 'create_item should call create method of CanvasNode'
        self.assertTrue(canvas.create.called, msg)

    @case('key', 1)
    @case('other_key', 'value')
    def test_setup_config_setter_calls_config(self, key, value):
        canvas = TestCanvasNode(Mock(), Mock())
        canvas.config = Mock()

        setup_config_setter(canvas)
        canvas.set_attr(key, value)

        msg = 'setup_config_setter should set setter that calls config method'
        self.assertEqual(canvas.config.call_args, call(**{key:value}), msg)

    def test_setup_event_binding_should_restore_bind(self):
        canvas = Mock()
        canvas.bind = Mock()

        setup_temp_binding(canvas)
        setup_event_binding(canvas)
        canvas.bind()

        msg = 'setup_event_binding should restore canvas bind method'
        self.assertTrue(canvas.bind.called, msg)

    @case({'key': lambda: None})
    @case({'key': lambda: None, 'two': lambda: None})
    def test_apply_temp_events_should_bind(self, events: dict):
        canvas = Mock()
        canvas.bind = Mock()
        canvas.events = events

        apply_temp_events(canvas)

        expected_calls = [call(event, command) for event, command in events.items()]
        msg = 'apply_temp_events should bind events stored in temp dictionary'
        self.assertEqual(canvas.bind.call_args_list, expected_calls, msg)

    def test_clear_temp_deletes_temp_vars(self):
        #pylint: disable=attribute-defined-outside-init
        canvas = TestCanvasNode(Mock(), Mock())
        canvas.attr_values = {}
        canvas.events = {}
        canvas.bind_source = {}

        clear_temp(canvas)

        msg = 'clear_temp should delete temp properties'
        self.assertFalse(hasattr(canvas, 'attr_values'), msg)
        self.assertFalse(hasattr(canvas, 'events'), msg)
        self.assertFalse(hasattr(canvas, 'bind_source'), msg)
