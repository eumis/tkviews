"""Runs sandbox application"""

from pyviews.rendering.pipeline import use_pipeline

from sandbox.widgets import get_scroll_pipeline
from tkviews.app import register_dependencies, launch


def run_sandbox():
    """Entry point"""
    register_dependencies()
    use_pipeline(get_scroll_pipeline(), 'sandbox.widgets')
    launch('app')


if __name__ == '__main__':
    run_sandbox()
