"""tkinter application entry point"""

from typing import cast

from injectool import add_singleton
from pyviews.binding import use_binding
from pyviews.code import run_code
from pyviews.containers import get_container_pipeline, get_view_pipeline, get_for_pipeline, \
    get_if_pipeline
from pyviews.presenter import get_presenter_pipeline
from pyviews.rendering import RenderingPipeline, use_rendering, get_child_context
from pyviews.rendering.pipeline import use_pipeline
from pyviews.rendering.views import render_view

from tkviews.canvas import get_canvas_pipeline
from tkviews.core.rendering import TkRenderingContext, get_tk_child_context
from tkviews.styles import get_style_pipeline, get_styles_view_pipeline
from tkviews.widgets import get_root_pipeline, get_widget_pipeline, Root
from tkviews.widgets import use_variables_binding
from tkviews.widgets.ttk import get_ttk_style_pipeline


def register_dependencies():
    """Registers all dependencies needed for application"""
    use_rendering()
    use_binding()
    use_variables_binding()
    use_tkviews_pipelines()


def use_tkviews_pipelines():
    """Adds rendering pipelines for tkviews"""
    add_singleton(get_child_context, get_tk_child_context)
    use_pipeline(get_root_pipeline(), 'tkviews.Root')
    use_pipeline(get_widget_pipeline(), 'tkinter')
    use_pipeline(get_widget_pipeline(), 'tkinter.ttk')
    use_pipeline(get_presenter_pipeline(), 'tkviews.PresenterNode')

    use_pipeline(get_container_pipeline(), 'tkviews.Container')
    use_pipeline(get_view_pipeline(), 'tkviews.View')
    use_pipeline(get_for_pipeline(), 'tkviews.For')
    use_pipeline(get_if_pipeline(), 'tkviews.If')

    use_pipeline(get_style_pipeline(), 'tkviews.Style')
    use_pipeline(get_styles_view_pipeline(), 'tkviews.StylesView')
    use_pipeline(get_ttk_style_pipeline(), 'tkviews.TtkStyle')
    use_pipeline(get_canvas_pipeline(), 'tkviews.canvas')

    use_pipeline(RenderingPipeline(pipes=[run_code]), 'tkviews.Code')


def launch(root_view=None):
    """Runs application. Widgets are created from passed xml_files"""
    root_view = 'root' if root_view is None else root_view
    root: Root = cast(Root, render_view(root_view, TkRenderingContext()))
    root.instance.mainloop()
