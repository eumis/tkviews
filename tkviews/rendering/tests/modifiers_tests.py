from unittest.mock import Mock, call

from pytest import mark

from tkviews.rendering.modifiers import bind, bind_all, set_attr, config, visible


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
def test_set_attr(key, value):
    """set_attr() should call set_attr with passed parameters"""
    node = Mock(set_attr=Mock())

    set_attr(node, key, value)

    assert node.set_attr.call_args == call(key, value)


@mark.parametrize('key, value', [
    ('key', 1),
    ('other_key', 'value')
])
def test_config(key, value):
    """config() should call config of widget from WidgetNode with passed parameters"""
    node = Mock(instance=Mock())

    config(node, key, value)

    assert node.instance.config.call_args == call(**{key: value})


def test_visible_true():
    """visible() should call geometry apply if true"""
    node = Mock(geometry=Mock(), instance=Mock())

    visible(node, None, True)

    assert node.geometry.apply.call_args == call(node.instance)


def test_visible_false():
    """visible() should call geometry forget if false"""
    node = Mock(geometry=Mock(), instance=Mock())

    visible(node, None, False)

    assert node.geometry.forget.call_args == call(node.instance)
