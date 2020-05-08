"""tkinter application entry point"""

from typing import cast

from pyviews.binding import use_binding
from pyviews.code import run_code
from pyviews.rendering import RenderingPipeline, use_rendering
from pyviews.rendering.pipeline import use_pipeline
from pyviews.rendering.views import render_view

from tkviews.containers import get_container_setup, get_view_setup, get_for_setup, get_if_setup
from tkviews.core.rendering import TkRenderingContext
from tkviews.styles import get_style_pipeline, get_styles_view_pipeline
from tkviews.widgets import get_root_setup, get_widget_setup, Root
from tkviews.widgets import use_variables_binding
from tkviews.widgets.ttk import get_ttk_style_setup


def register_dependencies():
    """Registers all dependencies needed for application"""
    use_rendering()
    use_binding()
    use_variables_binding()
    use_tkviews_pipelines()


def use_tkviews_pipelines():
    """Adds rendering pipelines for tkviews"""
    use_pipeline(get_root_setup(), 'tkviews.Root')
    use_pipeline(get_widget_setup(), 'tkinter')
    use_pipeline(get_widget_setup(), 'tkinter.ttk')

    use_pipeline(get_container_setup(), 'tkviews.Container')
    use_pipeline(get_view_setup(), 'tkviews.View')
    use_pipeline(get_for_setup(), 'tkviews.For')
    use_pipeline(get_if_setup(), 'tkviews.If')

    use_pipeline(get_style_pipeline(), 'tkviews.Style')
    use_pipeline(get_styles_view_pipeline(), 'tkviews.StylesView')
    use_pipeline(get_ttk_style_setup(), 'tkviews.TtkStyle')

    use_pipeline(RenderingPipeline(pipes=[run_code]), 'tkviews.Code')


def launch(root_view=None):
    """Runs application. Widgets are created from passed xml_files"""
    root_view = 'root' if root_view is None else root_view
    root: Root = cast(Root, render_view(root_view, TkRenderingContext()))
    root.instance.mainloop()
