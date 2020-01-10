"""tkinter application entry point"""

from os.path import abspath

from injectool import add_singleton, SingletonResolver, add_resolver, add_function_resolver
from pyviews.binding import Binder, OnceRule, OnewayRule
from pyviews.rendering import RenderingPipeline
from pyviews.code import run_code
from pyviews.rendering.views import render_view

from tkviews.binding import add_variables_rules
from tkviews.node import EntryNode, CheckbuttonNode, RadiobuttonNode
from tkviews.rendering import get_root_setup, get_widget_setup
from tkviews.rendering import get_container_setup, get_view_setup
from tkviews.rendering import get_for_setup, get_if_setup
from tkviews.rendering import get_style_setup
from tkviews.rendering import get_ttk_style_setup
from tkviews.rendering import get_layout_setup
from tkviews.rendering.common import TkRenderingContext


def register_dependencies():
    """Registers all dependencies needed for application"""
    add_singleton('views_folder', abspath('views'))
    add_singleton('view_ext', 'xml')
    add_singleton('namespaces', {'': 'tkinter'})
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

    pipeline_resolver.set_value(get_root_setup(), 'tkviews.Root')
    pipeline_resolver.set_value(get_widget_setup(), 'tkinter')
    pipeline_resolver.set_value(get_widget_setup(), EntryNode)
    pipeline_resolver.set_value(get_widget_setup(), CheckbuttonNode)
    pipeline_resolver.set_value(get_widget_setup(), RadiobuttonNode)
    pipeline_resolver.set_value(get_widget_setup(), 'tkinter.ttk')

    pipeline_resolver.set_value(get_container_setup(), 'tkviews.Container')
    pipeline_resolver.set_value(get_view_setup(), 'tkviews.View')
    pipeline_resolver.set_value(get_for_setup(), 'tkviews.For')
    pipeline_resolver.set_value(get_if_setup(), 'tkviews.If')

    pipeline_resolver.set_value(get_style_setup(), 'tkviews.Style')
    pipeline_resolver.set_value(get_ttk_style_setup(), 'tkviews.TtkStyle')

    pipeline_resolver.set_value(get_layout_setup(), 'tkviews.Row')
    pipeline_resolver.set_value(get_layout_setup(), 'tkviews.Column')

    pipeline_resolver.set_value(RenderingPipeline(pipes=[run_code]), 'tkviews.Code')

    return pipeline_resolver


def launch(root_view=None):
    """Runs application. Widgets are created from passed xml_files"""
    root_view = 'root' if root_view is None else root_view
    root = render_view(root_view, TkRenderingContext()).run()
    root.instance.mainloop()
