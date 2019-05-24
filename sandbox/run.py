"""Runs sandbox application"""
from injectool import register_single
from pyviews.rendering import RenderingPipeline

from tkviews.app import register_dependencies, launch
from sandbox.widgets import get_scroll_pipeline, Scroll


def run_sandbox():
    """Entry point"""
    register_dependencies()
    register_single(RenderingPipeline, get_scroll_pipeline(), Scroll)
    launch('app')


if __name__ == '__main__':
    run_sandbox()
