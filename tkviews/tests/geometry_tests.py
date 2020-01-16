from unittest.mock import Mock, call

from pytest import mark, fixture

from tkviews import WidgetNode
from tkviews.core.common import TkRenderingContext
from tkviews.geometry import GridGeometry, PackGeometry, PlaceGeometry, apply_layout, set_geometry


@fixture
def geometry_fixture(request):
    widget = Mock()
    widget.grid = Mock(grid_forget=Mock(), pack_forget=Mock())
    request.cls.widget = widget


@mark.usefixtures('geometry_fixture')
class GridGeometryTests:
    """GridGeometry class tests"""

    def test_apply(self):
        """should call grid method of widget"""
        geometry = GridGeometry()

        geometry.apply(self.widget)

        assert self.widget.grid.called
        assert self.widget.grid.call_count == 1

    def test_forget(self):
        """should call grid_forget method of widget"""
        geometry = GridGeometry()

        geometry.forget(self.widget)

        assert self.widget.grid_forget.called
        assert self.widget.grid_forget.call_count == 1

    @mark.parametrize('args', [
        {},
        {'row': 1, 'column': 1}
    ])
    def test_init(self, args):
        """grid should be called with arguments passed to geometry"""
        geometry = GridGeometry(**args)

        geometry.apply(self.widget)

        assert self.widget.grid.call_args == call(**args)

    @mark.parametrize('args', [
        {'row': 1},
        {'row': 1, 'column': 2},
        {'some_key': 'value'}
    ])
    def test_set(self, args):
        """grid should be called with arguments passed to geometry"""
        geometry = GridGeometry()

        for key, value in args.items():
            geometry.set(key, value)

        geometry.apply(self.widget)
        assert self.widget.grid.call_args == call(**args)


@mark.usefixtures('geometry_fixture')
class PackGeometryTests:
    """PackGeometry class tests"""

    def test_apply(self):
        """apply() should call pack method of widget"""
        geometry = PackGeometry()

        geometry.apply(self.widget)

        assert self.widget.pack.called
        assert self.widget.pack.call_count == 1

    def test_forget(self):
        """forget() should call pack_forget method of widget"""
        geometry = PackGeometry()

        geometry.forget(self.widget)

        assert self.widget.pack_forget.called

    @mark.parametrize('args', [
        {},
        {'expand': True, 'fill': 'x'}
    ])
    def test_init(self, args):
        """__init__() should call Widget.pack() with arguments passed to geometry"""
        geometry = PackGeometry(**args)

        geometry.apply(self.widget)

        assert self.widget.pack.call_args == call(**args)

    @mark.parametrize('args', [
        {'expand': True},
        {'expand': True, 'fill': 'x'},
        {'some_key': 'value'}
    ])
    def test_set(self, args):
        """set() should call Widget.pack() with arguments passed to geometry"""
        geometry = PackGeometry()

        for key, value in args.items():
            geometry.set(key, value)

        geometry.apply(self.widget)
        assert self.widget.pack.call_args == call(**args)


@mark.usefixtures('geometry_fixture')
class PlaceGeometryTests:
    """PlaceGeometry class tests"""

    def test_apply(self):
        """apply() should call pack method of widget"""
        geometry = PlaceGeometry()

        geometry.apply(self.widget)

        assert self.widget.place.called
        assert self.widget.place.call_count == 1

    def test_forget(self):
        """forget() should call place_forget method of widget"""
        geometry = PlaceGeometry()

        geometry.forget(self.widget)

        assert self.widget.place_forget.called

    @mark.parametrize('args', [
        {},
        {'expand': True, 'fill': 'x'}
    ])
    def test_init(self, args):
        """__init__() should call Widget.place() with arguments passed to geometry"""
        geometry = PlaceGeometry(**args)

        geometry.apply(self.widget)

        assert self.widget.place.call_args == call(**args)

    @mark.parametrize('args', [
        {'expand': True},
        {'expand': True, 'fill': 'x'},
        {'some_key': 'value'}
    ])
    def test_set(self, args):
        """set() should call Widget.place() with arguments passed to geometry"""
        geometry = PlaceGeometry()

        for key, value in args.items():
            geometry.set(key, value)

        geometry.apply(self.widget)
        assert self.widget.place.call_args == call(**args)


def test_apply_layout():
    """should call apply() method"""
    node = Mock()

    apply_layout(node, TkRenderingContext())

    assert node.apply.called


def test_set_geometry():
    """should apply geometry for node"""
    node, geometry = WidgetNode(Mock(), Mock()), Mock()

    set_geometry(node, 'key', geometry)

    assert geometry.apply.call_args == call(node.instance)
