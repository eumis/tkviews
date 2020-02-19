"""Widgets functionality"""

from .binding import VariableBinding, add_variables_rules
from .binding import bind_variable_and_expression, bind_custom_variable_and_expression
from .node import Root, get_root_setup, WidgetNode, get_widget_setup, setup_widget_setter, \
    setup_widget_destroy, apply_text, render_widget_children
from .setters import bind, bind_all, config
from .ttk import TtkWidgetNode, TtkStyle
