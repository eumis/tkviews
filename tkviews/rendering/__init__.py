'''Rendering'''

from pyviews.rendering import inject_global, import_global, set_global
from .canvas import get_canvas_setup
from .containers import get_container_setup, get_view_setup, get_for_setup, get_if_setup
from .geometry import get_layout_setup
from .modifiers import bind, bind_all, set_attr, config, visible
from .node import create_widget_node
from .styles import get_style_setup
from .ttk import get_ttk_style_setup
from .widgets import get_root_setup, get_widget_setup
