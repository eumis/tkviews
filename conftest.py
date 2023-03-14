# pylint: disable=unused-argument,redefined-outer-name

from injectool import use_container
from pytest import fixture
from pyviews.binding.setup import use_binding

from tkviews.widgets import use_variables_binding


@fixture
def container_fixture(request):
    """runs test in own dependency container"""
    with use_container() as container:
        if request.cls:
            request.cls.container = container
        yield container


@fixture
def binder_fixture(container_fixture):
    use_binding()
    use_variables_binding()
