'''
Nodes used as abstract containers, that used to incapsulate some logic.
Containers don't represent any widget.
'''

from pyviews.core.ioc import inject
from pyviews.core.xml import XmlNode
from pyviews.core.observable import InheritedDict
from pyviews.core.node import Node
from pyviews.rendering.views import get_view_root

class Container(Node):
    '''Used to combine some xml elements'''
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(xml_node, parent_context)
        self.master = master

    def set_attr(self, key, value):
        '''Sets passed attribute'''
        setattr(self, key, value)

    def get_render_args(self, xml_node):
        return TkRenderArgs(xml_node, self, self.master)

class View(Container):
    '''Loads xml from anothre file'''
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(master, xml_node, parent_context)
        self._name = None
        self._rendered = False

    @property
    def name(self):
        '''Relative view path'''
        return self._name

    @name.setter
    def name(self, value):
        if self._name == value:
            return
        self._name = value
        if self._rendered:
            self.render_children()

    @inject('render')
    def render_children(self, render=None):
        self._rendered = True
        self.destroy_children()
        if self.name is not None:
            root_xml = get_view_root(self.name)
            self._child_nodes = [render(root_xml, self.get_render_args(root_xml))]

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
            overflow = self._child_nodes[children_count:]
            for child in overflow:
                child.destroy()
            self._child_nodes = self._child_nodes[:children_count]
        except IndexError:
            pass

    def _update_existing(self):
        try:
            for index, item in enumerate(self._items):
                start = index * self._child_count
                end = (index + 1) * self._child_count
                for child_index in range(start, end):
                    globs = self._child_nodes[child_index].globals
                    globs['item'] = item
        except IndexError:
            pass

    def _create_not_existing(self):
        start = int(len(self._child_nodes) / self._child_count)
        end = len(self._items)
        self._render_children([(i, self._items[i]) for i in range(start, end)])

    @inject('render')
    def _render_children(self, items, render=None):
        nodes = self.xml_node.children
        for index, item in items:
            for xml_node in nodes:
                args = self.get_render_args(xml_node, index, item)
                self._child_nodes.append(render(xml_node, args))

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
