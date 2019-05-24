"""tkinter application entry point"""

from os.path import abspath

from injectool import register_single, register_func
from pyviews.binding import Binder, OnceRule, OnewayRule
from pyviews.compilation import CompiledExpression
from pyviews.core import Expression, render, create_node
from pyviews.rendering import render_node, render_view, RenderingPipeline
from pyviews.code import Code, run_code
from tkviews.binding import add_variables_rules
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
from tkviews.rendering import create_widget_node


def register_dependencies():
    """Registers all dependencies needed for application"""
    register_single('views_folder', abspath('views'))
    register_single('view_ext', 'xml')
    register_single('namespaces', {'': 'tkinter'})
    register_func(create_node, create_widget_node)
    register_func(render, render_node)
    register_func(Expression, CompiledExpression)
    register_single(Binder, setup_binder())

    register_single(RenderingPipeline, get_root_setup(), Root)
    register_single(RenderingPipeline, get_widget_setup(), WidgetNode)
    register_single(RenderingPipeline, get_widget_setup(), EntryNode)
    register_single(RenderingPipeline, get_widget_setup(), CheckbuttonNode)
    register_single(RenderingPipeline, get_widget_setup(), RadiobuttonNode)
    register_single(RenderingPipeline, get_widget_setup(), TtkWidgetNode)

    register_single(RenderingPipeline, get_container_setup(), Container)
    register_single(RenderingPipeline, get_view_setup(), View)
    register_single(RenderingPipeline, get_for_setup(), For)
    register_single(RenderingPipeline, get_if_setup(), If)

    register_single(RenderingPipeline, get_style_setup(), Style)
    register_single(RenderingPipeline, get_ttk_style_setup(), TtkStyle)

    register_single(RenderingPipeline, get_layout_setup(), Row)
    register_single(RenderingPipeline, get_layout_setup(), Column)

    register_single(RenderingPipeline, RenderingPipeline(steps=[run_code]), Code)


def setup_binder() -> Binder:
    """Adds all needed rules to binder"""
    binder = Binder()
    binder.add_rule('once', OnceRule())
    binder.add_rule('oneway', OnewayRule())
    add_variables_rules(binder)
    return binder


def launch(root_view=None):
    """Runs application. Widgets are created from passed xml_files"""
    root_view = 'root' if root_view is None else root_view
    root = render_view(root_view)
    root.instance.mainloop()
