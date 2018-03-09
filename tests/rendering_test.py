from unittest import TestCase, main
from unittest.mock import patch, Mock
from pyviews.testing import case
from tkviews import rendering

class ParsingTests(TestCase):
    @patch('tkviews.rendering.apply_attribute')
    @case(None)
    @case('')
    def test_apply_text_none(self, apply_attribute, text):
        node = Mock()
        node.xml_node = Mock()
        node.xml_node.text = text

        rendering.apply_text(node)

        msg = "apply_attribute shouldn't be called if text is None"
        self.assertFalse(apply_attribute.called, msg)

    @patch('tkviews.rendering.apply_attribute')
    @case('  ')
    @case('asdfasdf')
    def test_apply_text(self, apply_attribute, text):
        node = Mock()
        node.xml_node = Mock()
        node.xml_node.text = text

        rendering.apply_text(node)

        msg = 'apply_attirbute should be called with XmlAttr "text"'
        self.assertEqual(apply_attribute.call_args[0][0], node, msg)

        msg = 'apply_attirbute should be called with XmlAttr "text"'
        attr = apply_attribute.call_args[0][1]
        self.assertEqual(attr.name, 'text', msg)
        self.assertEqual(attr.value, text, msg)

if __name__ == '__main__':
    main()
