"""Runs demo application"""
from os.path import abspath
from injectool import add_singleton
from tkviews.app import register_dependencies, launch


def run_demo():
    """Entry point"""
    register_dependencies()
    add_singleton('views_folder', abspath('.'))
    launch('app/demo')


if __name__ == '__main__':
    run_demo()
