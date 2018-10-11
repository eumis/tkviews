'''ttk specific implementation'''

from tkinter.ttk import Style, Widget
from pyviews.core.xml import XmlNode
from pyviews.core.node import Node, InstanceNode
from pyviews.core.observable import InheritedDict
from tkviews.core import TkNode

class TtkWidgetNode(InstanceNode, TkNode):
    '''Wrapper under ttk widget'''
    def __init__(self, widget: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(widget, xml_node, node_globals=node_globals)
        self._node_styles = InheritedDict(node_styles)

    @property
    def node_styles(self) -> InheritedDict:
        '''Returns node styles set'''
        return self._node_styles

    @property
    def ttkstyle(self):
        '''Returns ttk style'''
        return self.instance.cget('style')

    @ttkstyle.setter
    def ttkstyle(self, value):
        self.instance.config(style=value)

class TtkStyle(Node):
    '''Node for tkk style'''
    def __init__(self, xml_node, parent_context=None, parent_name=None):
        super().__init__(xml_node, parent_context)
        self.values = {}
        self._parent_name = parent_name
        self.name = None

    @property
    def full_name(self):
        '''Full name'''
        return '{0}.{1}'.format(self.name, self._parent_name) \
               if self._parent_name else self.name

    def set_attr(self, key, value):
        '''Applies passed attribute'''
        if hasattr(self, key):
            setattr(self, key, value)
        else:
            self.values[key] = value

def theme_use(node, key, value):
    '''Sets ttk style theme'''
    ttk_style = Style()
    ttk_style.theme_use(key)

def apply_ttk_style(node: TtkStyle):
    '''Sets style to widget'''
    ttk_style = Style()
    if not node.name:
        raise KeyError("style doesn't have name")
    ttk_style.configure(node.full_name, **node.values)
