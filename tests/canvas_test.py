from unittest import TestCase, main
from unittest.mock import Mock, call
from pyviews.testing import case
from tkviews.canvas import CanvasNode

class CanvasItem(CanvasNode):
    def _create(self):
        self._canvas.create_item(*self.place, **self._options)
        return 1

class CanvasNodeTest(TestCase):
    def setUp(self):
        self.canvas = Mock()
        self.canvas.create_item = Mock()
        self.canvas.itemconfig = Mock()
        self.canvas.tag_bind = Mock()

    @case([1, 0, 2], {'fill': 'black'})
    @case((1, 0, 2), {})
    @case([], {})
    @case((), {'fill': 'black'})
    def test_creation(self, place, options):
        item = CanvasItem(self.canvas, None, None)

        item.place = place
        for key, value in options.items():
            item.set_attr(key, value)
        item.render()

        msg = 'place and options should be passed to create method'
        self.assertEqual(self.canvas.create_item.call_args, call(*place, **options), msg)

        msg = "itemconfig shouldn't be called"
        self.assertFalse(self.canvas.itemconfig.called, msg)

    @case('fill', 'black')
    @case('bd', 1)
    def test_update_options(self, key, value):
        item = CanvasItem(self.canvas, None, None)
        item.place = []
        item.render()

        item.set_attr(key, value)

        msg = "itemconfig should be called with passed params"
        self.assertEqual(self.canvas.itemconfig.call_args, call(item.item_id, **{key: value}), msg)

    @case('Button-1', lambda: print(1))
    def test_bind(self, event, command):
        item = CanvasItem(self.canvas, None, None)
        item.place = []

        item.bind(event, command)
        item.render()

        msg = "tag_bind should be called with item_id and passed params"
        call_args = call(item.item_id, '<'+ event + '>', command)
        self.assertEqual(self.canvas.tag_bind.call_args, call_args, msg)

    @case('Button-1', lambda: print(1))
    def test_bind_rendered(self, event, command):
        item = CanvasItem(self.canvas, None, None)
        item.place = []
        item.render()

        item.bind(event, command)

        msg = "tag_bind should be called with item_id and passed params"
        call_args = call(item.item_id, '<'+ event + '>', command)
        self.assertEqual(self.canvas.tag_bind.call_args, call_args, msg)

if __name__ == '__main__':
    main()
