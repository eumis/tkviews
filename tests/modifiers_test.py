from unittest import TestCase, main
from unittest.mock import Mock, call
from tkviews.modifiers import bind, bind_all, set_attr, config, visible

class TkModifiersTests(TestCase):
    def setUp(self):
        self.node = Mock()

    def test_bind(self):
        event = 'event'
        command = lambda: None

        bind(self.node, event, command)

        msg = "bind should call bind of WidgetNode with passed parameters"
        self.assertEqual(self.node.bind.call_args, call(event, command), msg)

    def test_bind_all(self):
        event = 'event'
        command = lambda: None

        bind_all(self.node, event, command)

        msg = "bind_all should call bind_all of WidgetNode with passed parameters"
        self.assertEqual(self.node.bind_all.call_args, call(event, command), msg)

    def test_set_attr(self):
        key = 'key'
        value = 2

        set_attr(self.node, key, value)

        msg = "set_attr should call set_attr of WidgetNode with passed parameters"
        self.assertEqual(self.node.set_attr.call_args, call(key, value), msg)

    def test_config(self):
        key = 'key'
        value = 2

        config(self.node, key, value)

        msg = "config should call config of widget from WidgetNode with passed parameters"
        self.assertEqual(self.node.widget.config.call_args, call(**{key: value}), msg)

    def test_visible_true(self):
        visible(self.node, None, True)

        msg = "visible should call geometry apply if true"
        self.assertEqual(self.node.geometry.apply.call_args, call(self.node.widget), msg)

    def test_visible_false(self):
        visible(self.node, None, False)

        msg = "visible should call geometry forget if false"
        self.assertEqual(self.node.geometry.forget.call_args, call(self.node.widget), msg)

if __name__ == '__main__':
    main()
