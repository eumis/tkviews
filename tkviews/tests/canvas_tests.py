from unittest.mock import Mock, call

from pytest import fixture, mark

from tkviews.canvas import CanvasItemNode, setup_temp_setter, setup_temp_binding, create_item, \
    setup_config_setter, \
    setup_event_binding, apply_temp_events, clear_temp, Rectangle, Text, Image, Arc, Bitmap, Line, \
    Oval, Polygon, Window
from tkviews.core.rendering import TkRenderingContext


class TestCanvasItem(CanvasItemNode):
    def __init__(self, canvas, item_id):
        super().__init__(canvas, Mock())
        self._id = item_id
        self.options = None

    def _create(self, **options):
        self.options = options
        return self._id


@fixture
def canvas_fixture(request):
    canvas = Mock()
    request.cls.canvas = canvas
    request.cls.item = TestCanvasItem(canvas, 1)


@mark.usefixtures('canvas_fixture')
class CanvasNodeTests:
    """CanvasNode class tests"""

    canvas: Mock
    item: TestCanvasItem

    @mark.parametrize('event, command', [
        ('Button-1', lambda: None)
    ])
    def test_bind(self, event, command):
        """bind() should call tag_bind of canvas"""
        self.item.create()

        self.item.bind(event, command)

        call_args = call(self.item.item_id, '<' + event + '>', command)
        assert self.canvas.tag_bind.call_args == call_args

    @mark.parametrize('options', [
        {'option1': 1},
        {'option1': 1, 'option2': 'value'}
    ])
    def test_config(self, options: dict):
        """config() should call itemconfig of canvas"""
        self.item.create()

        self.item.config(**options)

        call_args = call(self.item.item_id, **options)
        assert self.canvas.itemconfig.call_args == call_args

    def test_destroy(self):
        """should call canvas.delete()"""
        self.item.create()

        self.item.destroy()

        assert self.canvas.delete.call_args == call(self.item.item_id)


@fixture
def canvas_items_fixture(request):
    request.cls.canvas = Mock()
    request.cls.options = {'one': 1, 'two': 'two'}


@mark.usefixtures('canvas_items_fixture')
class CanvasItemsTests:
    """Canvas items tests"""

    canvas: Mock
    options: dict

    def test_rectangle_create(self):
        """Rectangle tests"""
        rectangle = Rectangle(self.canvas, Mock())
        rectangle.place = [1, 2]

        rectangle.create(**self.options)

        assert self.canvas.create_rectangle.call_args == call(*rectangle.place, **self.options)

    def test_text_create(self):
        """Text tests"""
        text = Text(self.canvas, Mock())
        text.place = [1, 2]

        text.create(**self.options)

        assert self.canvas.create_text.call_args == call(*text.place, **self.options)

    def test_image_create(self):
        """Image tests"""
        image = Image(self.canvas, Mock())
        image.place = [1, 2]

        image.create(**self.options)

        assert self.canvas.create_image.call_args == call(*image.place, **self.options)

    def test_arc_create(self):
        """Arc tests"""
        arc = Arc(self.canvas, Mock())
        arc.place = [1, 2]

        arc.create(**self.options)

        assert self.canvas.create_arc.call_args == call(*arc.place, **self.options)

    def test_bitmap_create(self):
        """Bitmap tests"""
        bitmap = Bitmap(self.canvas, Mock())
        bitmap.place = [1, 2]

        bitmap.create(**self.options)

        assert self.canvas.create_bitmap.call_args == call(*bitmap.place, **self.options)

    def test_line_create(self):
        """Line tests"""
        line = Line(self.canvas, Mock())
        line.place = [1, 2]

        line.create(**self.options)

        assert self.canvas.create_line.call_args == call(*line.place, **self.options)

    def test_oval_create(self):
        """Oval tests"""
        oval = Oval(self.canvas, Mock())
        oval.place = [1, 2]

        oval.create(**self.options)

        assert self.canvas.create_oval.call_args == call(*oval.place, **self.options)

    def test_polygon_create(self):
        """Polygon tests"""
        polygon = Polygon(self.canvas, Mock())
        polygon.place = [1, 2]

        polygon.create(**self.options)

        assert self.canvas.create_polygon.call_args == call(*polygon.place, **self.options)

    def test_window_create(self):
        """Window tests"""
        window = Window(self.canvas, Mock())
        window.place = [1, 2]

        window.create(**self.options)

        assert self.canvas.create_window.call_args == call(*window.place, **self.options)


class TestCanvasNode(CanvasItemNode):
    def _create(self, **options):
        return "id"


@mark.parametrize('attrs', [
    {'key': 1},
    {'key': 1, 'one': 'one'},
    {'key': None, 'list': [1], 'obj': object()}
])
def test_setup_temp_setter(attrs: dict):
    """setup_temp_setter() should set setter that stores attrs it attr_values property"""
    canvas = TestCanvasNode(Mock(), Mock())

    setup_temp_setter(canvas, TkRenderingContext())

    for key, value in attrs.items():
        canvas.set_attr(key, value)
    assert canvas.attr_values == attrs


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


def test_create_item_calls_create():
    """create_item( should call create method of CanvasNode"""
    canvas = Mock()
    canvas.create = Mock()
    canvas.attr_values = {}

    create_item(canvas, TkRenderingContext())

    assert canvas.create.called


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


def test_setup_event_binding_should_restore_bind():
    """setup_event_binding() should restore canvas bind method"""
    canvas = Mock()
    canvas.bind = Mock()

    setup_temp_binding(canvas, TkRenderingContext())
    setup_event_binding(canvas, TkRenderingContext())
    canvas.bind()

    assert canvas.bind.called


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
