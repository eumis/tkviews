"""tkinter application entry point"""

from os.path import abspath
from pyviews.core import ioc, Binder
from pyviews.compilation import CompiledExpression
from pyviews.binding import add_one_way_rules
from pyviews.rendering import render_node, render_view, RenderingPipeline
from pyviews.code import Code, run_code
from tkviews.binding import add_two_ways_rules
from tkviews.node import Root, WidgetNode, EntryNode, CheckbuttonNode, RadiobuttonNode
from tkviews.node import Container, View, For, If
from tkviews.node import Style
from tkviews.node import TtkWidgetNode, TtkStyle
from tkviews.node import Row, Column
from tkviews.rendering import get_root_setup, get_widget_setup
from tkviews.rendering import get_container_setup, get_view_setup
from tkviews.rendering import get_for_setup, get_if_setup
from tkviews.rendering import get_style_setup
from tkviews.rendering import get_ttk_style_setup
from tkviews.rendering import get_layout_setup
from tkviews.rendering import create_node


def register_dependencies():
    """Registers all dependencies needed for application"""
    ioc.register_single('views_folder', abspath('views'))
    ioc.register_single('view_ext', 'xml')
    ioc.register_single('namespaces', {'': 'tkinter'})
    ioc.register_func('create_node', create_node)
    ioc.register_func('render', render_node)
    ioc.register_func('expression', CompiledExpression)
    ioc.register_single('binder', setup_binder())

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

    ioc.register_single('pipeline', RenderingPipeline(steps=[run_code]), Code)


def setup_binder() -> Binder:
    """Adds all needed rules to binder"""
    binder = Binder()
    add_one_way_rules(binder)
    add_two_ways_rules(binder)
    return binder


def launch(root_view=None):
    """Runs application. Widgets are created from passed xml_files"""
    root_view = 'root' if root_view is None else root_view
    root = render_view(root_view)
    root.instance.mainloop()
