from tkinter import Widget

from pyviews.core import InheritedDict
from pyviews.rendering.common import RenderingContext


class TkRenderingContext(RenderingContext):
    @property
    def master(self) -> Widget:
        """master widget"""
        return self['master']

    @master.setter
    def master(self, value: Widget):
        self['master'] = value

    @property
    def node_styles(self) -> InheritedDict:
        return self['node_styles']

    @node_styles.setter
    def node_styles(self, value: InheritedDict):
        self['node_styles'] = value
