"""Runs sandbox application"""

from pyviews.rendering.pipeline import use_pipeline

from widgets import get_scroll_pipeline
from tkviews.app import launch, register_dependencies


def run_sandbox():
    """Entry point"""
    register_dependencies()
    use_pipeline(get_scroll_pipeline(), 'widgets')
    launch('app')


if __name__ == '__main__':
    run_sandbox()
