"""Layout nodes pipeline"""
from pyviews.pipes import apply_attributes
from pyviews.rendering import RenderingPipeline
from tkviews.node import LayoutSetup
from tkviews.rendering.common import TkRenderingContext


def get_layout_setup() -> RenderingPipeline:
    """Returns setup for canvas"""
    return RenderingPipeline(pipes=[
        apply_attributes,
        apply_layout
    ])


def apply_layout(node: LayoutSetup, _: TkRenderingContext):
    """Calls apply method"""
    node.apply()
