'''Core package'''

from pyviews import InheritedDict
from pyviews.core import get_not_implemented_message

class TkNode:
    '''Node interface'''
    @property
    def node_styles(self) -> InheritedDict:
        '''Returns node styles'''
        raise NotImplementedError(get_not_implemented_message(self, '_create'))
