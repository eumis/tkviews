"""Package adapts pyviews for using with tkinter"""

__version__ = '2.2.1'

from .containers import Container, View, For, If
from .styles import Style, StyleItem
from .ttk import TtkWidgetNode, TtkStyle
from .widgets import Root, WidgetNode, apply_styles
from .widgets import bind, bind_all, config

from pyviews.modifiers import import_global, set_global, inject_global, call, Args
