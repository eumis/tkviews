'''ttk specific implementation'''

from tkinter.ttk import Style as TtkStyle
from pyviews.core.node import Node
from pyviews.rendering.core import render_step
from tkviews.node import WidgetNode

class TtkWidgetNode(WidgetNode):
    '''Base wrapper for ttk widget'''
    @property
    def style(self):
        return self.widget.cget('style')

    @style.setter
    def style(self, value):
        self.widget.config(style=value)

class Style(Node):
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

    def get_render_args(self, xml_node):
        args = super().get_render_args(xml_node)
        args['parent_name'] = self.full_name
        return args

def theme_use(node, key, value):
    '''Sets ttk style theme'''
    ttk_style = TtkStyle()
    ttk_style.theme_use(key)

@render_step
def apply_ttk_style(node: Style):
    '''Sets style to widget'''
    ttk_style = TtkStyle()
    if not node.name:
        raise KeyError("style doesn't have name")
    ttk_style.configure(node.full_name, **node.values)
