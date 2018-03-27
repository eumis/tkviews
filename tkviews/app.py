'''tkinter application entry point'''

from os.path import abspath
from pyviews.core import ioc
from pyviews.rendering.dependencies import register_defaults
from pyviews.rendering.core import apply_attributes, render_children
from pyviews.rendering.binding import BindingFactory, add_default_rules
from pyviews.rendering.views import render_view
from tkviews.rendering import convert_to_node, apply_text
from tkviews.binding import add_rules as add_tkviews_binding_rules
from tkviews.modifiers import set_attr
from tkviews.styles import Style, apply_attributes as apply_style_attrs, apply_styles
from tkviews.geometry import Row, Column, apply_layout
from tkviews.node import Root
from tkviews.ttk import Style as TtkStyle, apply_ttk_style
from tkviews import canvas

def register_dependencies():
    '''Registers all dependencies needed for application'''
    register_defaults()
    ioc.register_single('views_folder', abspath('views'))
    ioc.register_single('view_ext', '.xml')
    ioc.register_single('styles', {})
    ioc.register_func('convert_to_node', convert_to_node)
    ioc.register_func('set_attr', set_attr)
    ioc.register_func('apply_styles', apply_styles)
    register_binding_factory()
    _register_rendering_steps()

def _register_rendering_steps():
    ioc.register_single('rendering_steps', [apply_attributes, apply_text, render_children])
    ioc.register_single('rendering_steps', [apply_attributes, render_children], Root)
    ioc.register_single('rendering_steps', [apply_style_attrs, render_children], Style)
    ioc.register_single('rendering_steps',
                        [apply_attributes, apply_ttk_style, render_children],
                        TtkStyle)
    ioc.register_single('rendering_steps', [apply_attributes, apply_layout], Row)
    ioc.register_single('rendering_steps', [apply_attributes, apply_layout], Column)
    _register_canvas_rendering_steps()

def _register_canvas_rendering_steps():
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Arc)
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Bitmap)
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Image)
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Line)
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Oval)
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Polygon)
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Rectangle)
    ioc.register_single('rendering_steps', [apply_attributes, apply_text, canvas.render], canvas.Text)
    ioc.register_single('rendering_steps', [apply_attributes, canvas.render], canvas.Window)

def register_binding_factory(factory=None):
    '''Adds all needed rules to binding factory and registers dependency'''
    factory = factory if factory else BindingFactory()
    add_default_rules(factory)
    add_tkviews_binding_rules(factory)
    ioc.register_single('binding_factory', factory)

def launch(root_view=None):
    '''Runs application. Widgets are created from passed xml_files'''
    root_view = 'root' if root_view is None else root_view
    root = render_view(root_view)
    root.widget.mainloop()
