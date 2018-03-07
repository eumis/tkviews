from unittest import TestCase, main
from unittest.mock import Mock
from tests.utility import case
from pyviews.core.observable import InheritedDict
from pyviews.core.compilation import CompilationError
from tkviews.code import Code

class CodeTests(TestCase):
    @case(
        '''
        def none():
            return None

        def one():
            return 1

        def str_value():
            return 'str_value'

        def global_key():
            return key
        ''',
        {'key': 'key'},
        {'none': None, 'one': 1, 'str_value': 'str_value', 'global_key': 'key'})
    def test_methods_definitions(self, content, globals_dict, expected):
        parent_globals = self._get_parent_globals(globals_dict)
        code = self._get_code_node(parent_globals, content)

        code.render_children()

        msg = 'defined functions should be added to parent globals'
        for key, value in expected.items():
            self.assertEqual(value, parent_globals[key](), msg)

    @case(
        '''
        one = 1
        str_value = 'str_value'
        global_key = key
        ''',
        {'key': 'key'},
        {'one': 1, 'str_value': 'str_value', 'global_key': 'key'})
    def test_variables_definitions(self, content, globals_dict, expected):
        parent_globals = self._get_parent_globals(globals_dict)
        code = self._get_code_node(parent_globals, content)

        code.render_children()

        msg = 'defined functions should be added to parent globals'
        for key, value in expected.items():
            self.assertEqual(value, parent_globals[key], msg)

    @case('''a = key.prop''', {'key': None})
    @case('''a = key.prop''', {})
    @case('''2/0''', {})
    @case(
        '''
        def some_func():
        pass
        ''', {})
    @case(
        '''
        def some_func()
            pass
        ''', {})
    def test_raises_error(self, content, globals_dict):
        parent_globals = self._get_parent_globals(globals_dict)
        code = self._get_code_node(parent_globals, content)

        msg = 'render_children should raise CompilationError for invalid code'
        with self.assertRaises(CompilationError, msg=msg):
            code.render_children()

    def _get_code_node(self, parent_globals, content):
        parent_node = Mock()
        parent_node.globals = parent_globals
        code = Code(parent_node, None)
        code.text = content
        return code

    def _get_parent_globals(self, globals_dict):
        parent_globals = InheritedDict()
        for key, value in globals_dict.items():
            parent_globals[key] = value
        return parent_globals

if __name__ == '__main__':
    main()
