'''Package adapts pyviews for using with tkinter'''

from pyviews.rendering.modifiers import set_global, import_global, inject_global
from .core.widgets import Root
from .core.containers import Container, For, View, If
from .core.styles import Style
from .core.geometry import Row, Column
from .core.canvas import Rectangle, Text, Image, Arc, Bitmap, Line, Oval, Polygon, Window
from .core.setters import bind, bind_all, set_attr, config, visible
