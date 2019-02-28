'''Base node type'''

from abc import ABC, abstractproperty
from pyviews.core import InheritedDict

class TkNode(ABC):
    '''Node interface'''
    @property
    @abstractproperty
    def node_styles(self) -> InheritedDict:
        '''Returns node styles'''