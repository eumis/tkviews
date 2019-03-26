#pylint: disable=missing-docstring

from unittest import TestCase
from unittest.mock import Mock, call
from pyviews.testing import case
from .canvas import CanvasNode

class CanvasItem(CanvasNode):
    def __init__(self, canvas, item_id):
        super().__init__(canvas, None)
        self._id = item_id
        self.options = None

    def _create(self, **options):
        self.options = options
        return self._id

class CanvasNodeTest(TestCase):
    def setUp(self):
        self.canvas = Mock()
        self.canvas.create_item = Mock()
        self.canvas.itemconfig = Mock()
        self.canvas.tag_bind = Mock()

    @case('Button-1', lambda: None)
    def test_bind_calls_canvas_tag_bind(self, event, command):
        item = CanvasItem(self.canvas, 1)
        item.create()

        item.bind(event, command)

        msg = 'bind should call tag_bind of canvas'
        call_args = call(item.item_id, '<'+ event + '>', command)
        self.assertEqual(self.canvas.tag_bind.call_args, call_args, msg)

    @case({'option1': 1})
    @case({'option1': 1, 'option2': 'value'})
    def test_config_calls_canvas_item_config(self, options: dict):
        item = CanvasItem(self.canvas, 1)
        item.create()

        item.config(**options)

        msg = 'config should call itemconfig of canvas'
        call_args = call(item.item_id, **options)
        self.assertEqual(self.canvas.itemconfig.call_args, call_args, msg)
