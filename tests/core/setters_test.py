from unittest import TestCase, main
from unittest.mock import Mock, call
from pyviews.testing import case
from tkviews.core.setters import bind, bind_all, set_attr, config, visible

class TkModifiersTests(TestCase):
    def test_bind(self):
        node = Mock(instance=Mock())

        bind(node, 'event', lambda: None)

        msg = "bind should call bind of instance"
        self.assertTrue(node.instance.bind.called, msg)

    def test_bind_all(self):
        node = Mock(instance=Mock())

        bind_all(node, 'event', lambda: None)

        msg = "bind_all should call bind_all of instance"
        self.assertTrue(node.instance.bind_all.called, msg)

    @case('key', 1)
    @case('other_key', 'value')
    def test_set_attr(self, key, value):
        node = Mock(setter=Mock())

        set_attr(node, key, value)

        msg = "set_attr should call setter with passed parameters"
        self.assertEqual(node.setter.call_args, call(node, key, value), msg)

    @case('key', 1)
    @case('other_key', 'value')
    def test_config(self, key, value):
        node = Mock(instance=Mock())

        config(node, key, value)

        msg = "config should call config of widget from WidgetNode with passed parameters"
        self.assertEqual(node.instance.config.call_args, call(**{key: value}), msg)

    def test_visible_true(self):
        node = Mock(geometry=Mock(), instance=Mock())

        visible(node, None, True)

        msg = "visible should call geometry apply if true"
        self.assertEqual(node.geometry.apply.call_args, call(node.instance), msg)

    def test_visible_false(self):
        node = Mock(geometry=Mock(), instance=Mock())

        visible(node, None, False)

        msg = "visible should call geometry forget if false"
        self.assertEqual(node.geometry.forget.call_args, call(node.instance), msg)

if __name__ == '__main__':
    main()
