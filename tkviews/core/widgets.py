'''Tkinter widgets nodes'''

from tkinter import Tk, Widget
from pyviews.core.xml import XmlNode
from pyviews.core.node import InstanceNode
from pyviews.core.observable import InheritedDict
from tkviews.core import TkNode

class Root(InstanceNode, TkNode):
    '''Wrapper under tkinter Root'''
    def __init__(self, xml_node: XmlNode):
        super().__init__(Tk(), xml_node)
        self._icon = None
        self._node_styles = InheritedDict()

    @property
    def node_styles(self) -> InheritedDict:
        '''Returns node styles set'''
        return self._node_styles

    @property
    def state(self):
        '''Widget state'''
        return self.widget.state()

    @state.setter
    def state(self, state):
        self.widget.state(state)

    @property
    def icon(self):
        '''Icon path'''
        return self._icon

    @icon.setter
    def icon(self, value):
        self._icon = value
        self.widget.iconbitmap(default=value)

class WidgetNode(InstanceNode, TkNode):
    '''Wrapper under tkinter widget'''
    def __init__(self, widget: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(widget, xml_node, node_globals=node_globals)
        self._node_styles = InheritedDict(node_styles)

    @property
    def node_styles(self) -> InheritedDict:
        '''Returns node styles set'''
        return self._node_styles
