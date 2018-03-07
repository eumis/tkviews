'''Module contains Code node'''

from sys import exc_info
from textwrap import dedent
from pyviews.core.node import Node
from pyviews.core.compilation import CompilationError

class Code(Node):
    '''Wrapper under python code inside view'''
    def __init__(self, parent_node, xml_node, parent_context=None):
        super().__init__(xml_node, parent_context)
        self._parent_globals = parent_node.globals
        self.text = ''

    def set_attr(self, key, value):
        '''sets attribute'''
        setattr(self, key, value)

    def render_children(self):
        '''Executes node content as python module and adds its definitions to globals'''
        try:
            globs = self._parent_globals.to_dictionary()
            exec(dedent(self.text), globs)
            definitions = [(key, value) for key, value in globs.items() \
                        if key != '__builtins__' and not self._parent_globals.has_key(key)]
            for key, value in definitions:
                self._parent_globals[key] = value
        except:
            info = exc_info()
            msg = 'Code execution is failed:\n{0}'.format(self.text)
            raise CompilationError(msg, str(info[1])) from info[1]
