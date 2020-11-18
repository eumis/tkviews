"""Package adapts pyviews for using with tkinter"""

__version__ = '3.1.0'

from pyviews.setters import import_global, inject_global, call, set_global, Args, call_args
from pyviews.code import Code
from pyviews.containers import Container, View, For, If
from pyviews.presenter import PresenterNode, add_reference

from .styles import Style, StylesView, StyleItem, apply_styles
from .widgets import WidgetNode, Root
from .widgets import TtkStyle
from .widgets import bind, bind_all, config
