"""Geometry managers wrappers"""

from abc import ABC, abstractmethod
from tkinter import Widget
from typing import Any


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
