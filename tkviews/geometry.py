"""Geometry managers wrappers"""

from abc import ABC, abstractmethod
from tkinter import Widget
from typing import Any

from pyviews.core import Node, XmlNode
from pyviews.pipes import apply_attributes
from pyviews.rendering import RenderingPipeline

from tkviews.widgets import WidgetNode
from tkviews.core.common import TkRenderingContext


class Geometry(ABC):
    """Base for wrapper"""

    def __init__(self, **args):
        self._args = args if args else {}

    def set(self, key: str, value: Any):
        """Sets geometry parameter"""
        self._args[key] = value

    @abstractmethod
    def apply(self, widget: Widget):
        """Applies geometry with passed parameters"""

    @abstractmethod
    def forget(self, widget: Widget):
        """Calls forget method for geometry"""


class GridGeometry(Geometry):
    """Grid geometry wrapper"""

    def apply(self, widget: Widget):
        widget.grid(**self._args)

    def forget(self, widget: Widget):
        widget.grid_forget()


class PackGeometry(Geometry):
    """Pack geometry wrapper"""

    def apply(self, widget: Widget):
        widget.pack(**self._args)

    def forget(self, widget: Widget):
        widget.pack_forget()


class PlaceGeometry(Geometry):
    """Place geometry wrapper"""

    def apply(self, widget: Widget):
        widget.place(**self._args)

    def forget(self, widget: Widget):
        widget.place_forget()


class LayoutSetup(Node, ABC):
    """Base for wrappers under methods calls of geometry"""

    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(xml_node, parent_context)
        self._master = master
        self.args = {}
        self.index = None

    def set_attr(self, key, value):
        """Sets config parameter"""
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.args[key] = value

    @abstractmethod
    def apply(self):
        """Calls config with passed parameters"""


class Row(LayoutSetup):
    """Wrapper under grid_rowconfigure method"""

    def apply(self):
        self._master.grid_rowconfigure(self.index, **self.args)


class Column(LayoutSetup):
    """Wrapper under grid_columnconfigure method"""

    def apply(self):
        self._master.grid_columnconfigure(self.index, **self.args)


def get_layout_setup() -> RenderingPipeline:
    """Returns setup for canvas"""
    return RenderingPipeline(pipes=[
        apply_attributes,
        apply_layout
    ])


def apply_layout(node: LayoutSetup, _: TkRenderingContext):
    """Calls apply method"""
    node.apply()


def set_geometry(node: WidgetNode, _: str, geometry: Geometry):
    if geometry is not None:
        geometry.apply(node.instance)
