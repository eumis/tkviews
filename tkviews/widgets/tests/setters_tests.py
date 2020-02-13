from unittest.mock import Mock, call

from pytest import mark

from tkviews.widgets.setters import bind, bind_all, config


def test_bind():
    """bind() should call bind for instance"""
    node = Mock()

    bind(node, 'event', lambda: None)

    assert node.bind.called


def test_bind_all():
    """bind_all() should call bind_all of instance"""
    node = Mock()

    bind_all(node, 'event', lambda: None)

    assert node.bind_all.called


@mark.parametrize('key, value', [
    ('key', 1),
    ('other_key', 'value')
])
def test_config(key, value):
    """config() should call config of widget from WidgetNode with passed parameters"""
    node = Mock(instance=Mock())

    config(node, key, value)

    assert node.instance.config.call_args == call(**{key: value})
