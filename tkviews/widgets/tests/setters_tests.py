from unittest.mock import Mock, call

from pytest import mark, raises

from tkviews.widgets.setters import bind, bind_all, config, CallbackError


class BindTests:
    @staticmethod
    def test_binds():
        """bind() should call bind for instance"""
        node = Mock()

        bind(node, 'event', lambda: None)

        assert node.bind.called

    @staticmethod
    def test_handles_error():
        """should raise CallbackError with event info"""

        def callback():
            raise ValueError()

        with raises(CallbackError):
            node_bind = Mock()
            node_bind.side_effect = lambda e, cb: cb()

            bind(Mock(bind=node_bind), 'event', callback)


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
