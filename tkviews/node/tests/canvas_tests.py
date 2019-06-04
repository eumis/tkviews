from unittest.mock import Mock, call

from pytest import fixture, mark

from tkviews.node.canvas import CanvasNode


class CanvasItem(CanvasNode):
    def __init__(self, canvas, item_id):
        super().__init__(canvas, None)
        self._id = item_id
        self.options = None

    def _create(self, **options):
        self.options = options
        return self._id


@fixture
def canvas_fixture(request):
    canvas = Mock()
    canvas.create_item = Mock()
    canvas.itemconfig = Mock()
    canvas.tag_bind = Mock()
    request.cls.canvas = canvas


@mark.usefixtures('canvas_fixture')
class CanvasNodeTests:
    """CanvasNode class tests"""

    @mark.parametrize('event, command', [
        ('Button-1', lambda: None)
    ])
    def test_bind(self, event, command):
        """bind() should call tag_bind of canvas"""
        item = CanvasItem(self.canvas, 1)
        item.create()

        item.bind(event, command)

        call_args = call(item.item_id, '<' + event + '>', command)
        assert self.canvas.tag_bind.call_args == call_args

    @mark.parametrize('options', [
        {'option1': 1},
        {'option1': 1, 'option2': 'value'}
    ])
    def test_config(self, options: dict):
        """config() should call itemconfig of canvas"""
        item = CanvasItem(self.canvas, 1)
        item.create()

        item.config(**options)

        call_args = call(item.item_id, **options)
        assert self.canvas.itemconfig.call_args == call_args
