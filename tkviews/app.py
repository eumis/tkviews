"""tkinter application entry point"""

from typing import Optional, cast

from injectool import add_singleton
from pyviews.binding.config import use_binding
from pyviews.code import run_code
from pyviews.containers import get_container_pipeline, get_for_pipeline, get_if_pipeline, get_view_pipeline
from pyviews.core.rendering import NodeGlobals
from pyviews.presenter import get_presenter_pipeline
from pyviews.rendering.context import get_child_context
from pyviews.rendering.pipeline import RenderingPipeline, render_view, use_pipeline
from pyviews.rendering.config import use_rendering

from tkviews.canvas import get_canvas_pipeline
from tkviews.core.rendering import TkRenderingContext, get_tk_child_context
from tkviews.listbox import get_listboxitem_pipeline
from tkviews.styles import get_style_pipeline, get_styles_view_pipeline
from tkviews.widgets import Root, get_root_pipeline, get_widget_pipeline, use_variables_binding
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
    use_pipeline(get_listboxitem_pipeline(), 'tkviews.ListboxItem')

    use_pipeline(RenderingPipeline(pipes = [run_code]), 'tkviews.Code')


def launch(root_view: str, view_globals: Optional[dict] = None):
    """Runs application. Widgets are created from passed xml_files"""
    root_view = 'root' if root_view is None else root_view
    rendering_context = TkRenderingContext({'node_globals': NodeGlobals(view_globals)} if view_globals else {})
    root: Root = cast(Root, render_view(root_view, rendering_context))
    root.instance.mainloop()
