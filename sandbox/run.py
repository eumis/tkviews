"""Runs sandbox application"""
from injectool import set_container, Container

from tkviews.app import register_dependencies, launch


def run_sandbox():
    """Entry point"""
    set_container(Container())
    register_dependencies()
    # resolver = get_pipeline_resolver()
    # resolver.set_value(get_scroll_pipeline(), Scroll)
    # add_resolver(RenderingPipeline, resolver)
    launch('app')


if __name__ == '__main__':
    run_sandbox()
