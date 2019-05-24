"""Layout nodes pipeline"""

from pyviews.rendering import RenderingPipeline, apply_attributes
from tkviews.node import LayoutSetup


def get_layout_setup() -> RenderingPipeline:
    """Returns setup for canvas"""
    return RenderingPipeline(steps=[
        setup_setter,
        apply_attributes,
        apply_layout
    ])


def setup_setter(node: LayoutSetup, **_):
    """Sets attributes setter"""
    node.attr_setter = _set_layout_attr


def _set_layout_attr(node: LayoutSetup, key, value):
    """Sets config parameter"""
    if hasattr(node, key):
        setattr(node, key, value)
    else:
        node.args[key] = value


def apply_layout(node: LayoutSetup, **_):
    """Calls apply method"""
    node.apply()
