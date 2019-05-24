"""Base node type"""

from abc import ABC, abstractmethod
from pyviews.core import InheritedDict


class TkNode(ABC):
    """Node interface"""

    @property
    @abstractmethod
    def node_styles(self) -> InheritedDict:
        """Returns node styles"""
