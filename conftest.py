# pylint: disable=unused-argument,redefined-outer-name

from injectool import use_container, set_container, Container, add_singleton
from pytest import fixture
from pyviews.binding import Binder

from tkviews.app import setup_binder


def pytest_configure(config):
    set_container(Container())


@fixture
def container_fixture(request):
    """runs test in own dependency container"""
    with use_container() as container:
        if request.cls:
            request.cls.container = container
        yield container


@fixture
def binder_fixture(container_fixture):
    add_singleton(Binder, setup_binder())
