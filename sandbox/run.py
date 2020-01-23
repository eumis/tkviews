"""Runs sandbox application"""
from tkinter import Entry

from injectool import set_container, Container, add_resolver, resolve, add_singleton
from pyviews.binding import Binder
from pyviews.rendering import RenderingPipeline

from sandbox.variables import IntVar
from sandbox.widgets import get_scroll_pipeline
from tkviews.app import register_dependencies, launch, get_pipeline_resolver
from tkviews.widgets import VariableTwowaysRule
from cProfile import Profile


def run_sandbox():
    """Entry point"""
    set_container(Container())
    register_dependencies()
    resolver = get_pipeline_resolver()
    resolver.set_value(get_scroll_pipeline(), 'sandbox.widgets')
    add_resolver(RenderingPipeline, resolver)
    binder = resolve(Binder)
    binder.add_rule('int_var', VariableTwowaysRule(Entry, 'textvariable', IntVar))

    profile = Profile()
    add_singleton(Profile, profile)
    launch('app')
    profile.print_stats('pcall')


if __name__ == '__main__':
    run_sandbox()
