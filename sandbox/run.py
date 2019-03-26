'''Runs sandbox application'''

from pyviews.core.ioc import register_single
from tkviews.app import register_dependencies, launch
from widgets import get_scroll_pipeline, Scroll

def run_sandbox():
    '''Entry point'''
    register_dependencies()
    register_single('pipeline', get_scroll_pipeline(), Scroll)
    launch('app')

if __name__ == '__main__':
    run_sandbox()
