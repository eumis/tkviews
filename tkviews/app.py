"""tkinter application entry point"""

from os.path import abspath

from injectool import add_singleton, SingletonResolver, add_resolver, add_resolve_function
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
    add_singleton('views_folder', abspath('views'))
    add_singleton('view_ext', 'xml')
    add_singleton('namespaces', {'': 'tkinter'})
    add_singleton(create_node, create_widget_node)
    add_singleton(render, render_node)
    add_resolve_function(Expression, lambda c, p: CompiledExpression(p))
    add_singleton(Binder, setup_binder())
    add_resolver(RenderingPipeline, get_pipeline_resolver())


def setup_binder() -> Binder:
    """Adds all needed rules to binder"""
    binder = Binder()
    binder.add_rule('once', OnceRule())
    binder.add_rule('oneway', OnewayRule())
    add_variables_rules(binder)
    return binder


def get_pipeline_resolver() -> SingletonResolver:
    pipeline_resolver = SingletonResolver()

    pipeline_resolver.add_value(get_root_setup(), Root)
    pipeline_resolver.add_value(get_widget_setup(), WidgetNode)
    pipeline_resolver.add_value(get_widget_setup(), EntryNode)
    pipeline_resolver.add_value(get_widget_setup(), CheckbuttonNode)
    pipeline_resolver.add_value(get_widget_setup(), RadiobuttonNode)
    pipeline_resolver.add_value(get_widget_setup(), TtkWidgetNode)

    pipeline_resolver.add_value(get_container_setup(), Container)
    pipeline_resolver.add_value(get_view_setup(), View)
    pipeline_resolver.add_value(get_for_setup(), For)
    pipeline_resolver.add_value(get_if_setup(), If)

    pipeline_resolver.add_value(get_style_setup(), Style)
    pipeline_resolver.add_value(get_ttk_style_setup(), TtkStyle)

    pipeline_resolver.add_value(get_layout_setup(), Row)
    pipeline_resolver.add_value(get_layout_setup(), Column)

    pipeline_resolver.add_value(RenderingPipeline(steps=[run_code]), Code)

    return pipeline_resolver


def launch(root_view=None):
    """Runs application. Widgets are created from passed xml_files"""
    root_view = 'root' if root_view is None else root_view
    root = render_view(root_view)
    root.instance.mainloop()
