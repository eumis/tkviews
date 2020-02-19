"""Package adapts pyviews for using with tkinter"""

__version__ = '2.2.1'

# noinspection PyUnresolvedReferences
from pyviews.setters import import_global, inject_global, call, set_global, Args, call_args

from .containers import Container, View, For, If
from .styles import Style, StyleItem, apply_styles
from .widgets import WidgetNode, Root
from .widgets import TtkWidgetNode, TtkStyle
from .widgets import bind, bind_all, config
