"""Runs sandbox application"""

from injectool import set_container, Container, add_resolver
from pyviews.rendering import RenderingPipeline

from sandbox.widgets import get_scroll_pipeline
from tkviews.app import register_dependencies, launch, get_pipeline_resolver


def run_sandbox():
    """Entry point"""
    set_container(Container())
    register_dependencies()
    resolver = get_pipeline_resolver()
    resolver.set_value(get_scroll_pipeline(), 'sandbox.widgets')
    add_resolver(RenderingPipeline, resolver)
    launch('app')


if __name__ == '__main__':
    run_sandbox()
