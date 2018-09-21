'''
Nodes used as abstract containers, that used to incapsulate some logic.
Containers don't represent any widget.
'''

from tkinter import Widget
from pyviews.core.ioc import inject
from pyviews.core.xml import XmlNode
from pyviews.core.observable import InheritedDict, observable_property
from pyviews.core.node import Node

class Container(Node):
    '''Used to combine some xml elements'''
    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self.master = master
        self.styles = node_styles

class View(Node):
    '''Loads xml from anothre file'''
    def __init__(self, master: Widget, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self.master = master
        self.node_styles = node_styles

    (name, name_observable) = observable_property('_name')

    def set_content(self, content: Node):
        '''Destroys current '''
        self._children = [content]

class For(Container):
    '''Renders children for every item in items collection'''
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(master, xml_node, parent_context)
        self._items = []
        self._rendered = False
        self._child_count = 0

    @property
    def items(self):
        '''Source collection'''
        return self._items

    @items.setter
    def items(self, val):
        self._items = val
        if self._rendered:
            self._destroy_overflow()
            self._update_existing()
            self._create_not_existing()

    def _destroy_overflow(self):
        try:
            items_count = len(self._items)
            children_count = self._child_count * items_count
            overflow = self._children[children_count:]
            for child in overflow:
                child.destroy()
            self._children = self._children[:children_count]
        except IndexError:
            pass

    def _update_existing(self):
        try:
            for index, item in enumerate(self._items):
                start = index * self._child_count
                end = (index + 1) * self._child_count
                for child_index in range(start, end):
                    globs = self._children[child_index].globals
                    globs['item'] = item
        except IndexError:
            pass

    def _create_not_existing(self):
        start = int(len(self._children) / self._child_count)
        end = len(self._items)
        self._render_children([(i, self._items[i]) for i in range(start, end)])

    @inject('render')
    def _render_children(self, items, render=None):
        nodes = self.xml_node.children
        for index, item in items:
            for xml_node in nodes:
                args = self.get_render_args(xml_node, index, item)
                self._children.append(render(xml_node, args))

    def render_children(self):
        self._rendered = True
        self._child_count = len(self.xml_node.children)
        self.destroy_children()
        self._render_children([(i, item) for i, item in enumerate(self._items)])

    def get_render_args(self, xml_node: XmlNode, index=None, item=None):
        args = super().get_render_args(xml_node)
        context = args['parent_context'].copy()
        item_globals = InheritedDict(context['globals'])
        item_globals['index'] = index
        item_globals['item'] = item
        context['globals'] = item_globals
        args['parent_context'] = context
        return args

class If(Container):
    '''Renders children if condition is True'''
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(master, xml_node, parent_context)
        self._condition = False
        self._rendered = False

    @property
    def condition(self):
        '''Condition of rendering'''
        return self._condition

    @condition.setter
    def condition(self, value):
        if self._condition == value:
            return
        self._condition = value
        if self._rendered:
            self.destroy_children()
            self.render_children()

    def render_children(self):
        if self._condition:
            super().render_children()
        self._rendered = True
