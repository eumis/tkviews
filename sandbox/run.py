"""Runs sandbox application"""
from injectool import add_resolver
from pyviews.rendering import RenderingPipeline

from tkviews.app import register_dependencies, launch, get_pipeline_resolver
from sandbox.widgets import get_scroll_pipeline, Scroll


def run_sandbox():
    """Entry point"""
    register_dependencies()
    resolver = get_pipeline_resolver()
    resolver.set_value(get_scroll_pipeline(), Scroll)
    add_resolver(RenderingPipeline, resolver)
    launch('app')


if __name__ == '__main__':
    run_sandbox()
