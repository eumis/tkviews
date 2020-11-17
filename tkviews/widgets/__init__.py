"""Widgets functionality"""

from .binding import VariableBinding, use_variables_binding
from .binding import bind_variable_and_expression, bind_custom_variable_and_expression
from .node import Root, get_root_pipeline, WidgetNode, get_widget_pipeline, setup_widget_setter, \
    setup_widget_destroy, apply_text, render_widget_children
from .setters import bind, bind_all, config
from .ttk import TtkStyle
