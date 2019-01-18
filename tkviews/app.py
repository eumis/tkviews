'''tkinter application entry point'''

from os.path import abspath
from pyviews.core import ioc
from pyviews.dependencies import register_defaults
from pyviews.rendering.binding import Binder, add_default_rules
from pyviews.rendering.views import render_view
from tkviews.rendering import create_node
from tkviews.core.binding import add_rules as add_tkviews_binding_rules
from tkviews.core.widgets import Root, WidgetNode, EntryNode, CheckbuttonNode, RadiobuttonNode
from tkviews.core.containers import Container, View, For, If
from tkviews.core.styles import Style
from tkviews.core.ttk import TtkWidgetNode, TtkStyle
from tkviews.core.geometry import Row, Column
from tkviews.setup.widgets import get_root_setup, get_widget_setup
from tkviews.setup.containers import get_container_setup, get_view_setup
from tkviews.setup.containers import get_for_setup, get_if_setup
from tkviews.setup.styles import get_style_setup
from tkviews.setup.ttk import get_ttk_style_setup
from tkviews.setup.geometry import get_layout_setup

def register_dependencies():
    '''Registers all dependencies needed for application'''
    register_defaults()
    ioc.register_single('views_folder', abspath('views'))
    ioc.register_single('view_ext', 'xml')
    ioc.register_func('create_node', create_node)

    ioc.register_single('pipeline', get_root_setup(), Root)
    ioc.register_single('pipeline', get_widget_setup(), WidgetNode)
    ioc.register_single('pipeline', get_widget_setup(), EntryNode)
    ioc.register_single('pipeline', get_widget_setup(), CheckbuttonNode)
    ioc.register_single('pipeline', get_widget_setup(), RadiobuttonNode)
    ioc.register_single('pipeline', get_widget_setup(), TtkWidgetNode)

    ioc.register_single('pipeline', get_container_setup(), Container)
    ioc.register_single('pipeline', get_view_setup(), View)
    ioc.register_single('pipeline', get_for_setup(), For)
    ioc.register_single('pipeline', get_if_setup(), If)

    ioc.register_single('pipeline', get_style_setup(), Style)
    ioc.register_single('pipeline', get_ttk_style_setup(), TtkStyle)

    ioc.register_single('pipeline', get_layout_setup(), Row)
    ioc.register_single('pipeline', get_layout_setup(), Column)

    register_binder()

# def _register_rendering_steps():
#     ioc.register_single('rendering_steps', [apply_style_attrs, render_children], Style)
#     ioc.register_single('rendering_steps',
#                         [apply_attributes, apply_ttk_style, render_children],
#                         TtkStyle)
#     ioc.register_single('rendering_steps', [apply_attributes, apply_layout], Row)
#     ioc.register_single('rendering_steps', [apply_attributes, apply_layout], Column)
#     _register_canvas_rendering_steps()

# def _register_canvas_rendering_steps():
#     canvas_node_types = [
#         canvas.Arc, canvas.Bitmap, canvas.Image,
#         canvas.Line, canvas.Oval, canvas.Polygon,
#         canvas.Rectangle, canvas.Window
#     ]
#     for node_type in canvas_node_types:
#         ioc.register_single('rendering_steps', [apply_attributes, canvas.render], node_type)
#     ioc.register_single(
#         'rendering_steps',
#         [apply_attributes, apply_text, canvas.render],
#         canvas.Text)

def register_binder(binder: Binder = None):
    '''Adds all needed rules to binding factory and registers dependency'''
    binder = binder if binder else Binder()
    add_default_rules(binder)
    add_tkviews_binding_rules(binder)
    ioc.register_single('binder', binder)

def launch(root_view=None):
    '''Runs application. Widgets are created from passed xml_files'''
    root_view = 'root' if root_view is None else root_view
    root = render_view(root_view)
    root.instance.mainloop()
