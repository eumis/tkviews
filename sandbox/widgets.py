from tkinter import Frame, Canvas, Scrollbar
from pyviews.core.observable import InheritedDict
from pyviews.core.xml import XmlNode
from pyviews.rendering.pipeline import RenderingPipeline, render_children, apply_attributes
from pyviews.core.node import Node
from tkviews.core import TkNode


class Scroll(Node, TkNode):
    def __init__(self, master, xml_node: XmlNode,
                 node_globals: InheritedDict = None, node_styles: InheritedDict = None):
        super().__init__(xml_node, node_globals=node_globals)
        self._frame = self._create_scroll_frame(master)
        self._canvas = self._create_canvas(self._frame)
        self._scroll = self._create_scroll(self._frame, self._canvas)
        self._container = self._create_container(self._canvas)
        self._container.bind('<Configure>', lambda event: self._config_container())
        self._canvas.bind('<Configure>', self._config_canvas)
        self._canvas.bind_all('<MouseWheel>', self._on_mouse_scroll)
        self._canvas.bind('<Enter>', lambda event: self._set_canvas_active())
        self._canvas.bind('<Leave>', lambda event: self._set_canvas_inactive())
        self._geometry = None
        self._node_styles = node_styles

    @staticmethod
    def _create_scroll_frame(master):
        frame = Frame(master)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return frame

    @staticmethod
    def _create_canvas(master):
        canvas = Canvas(master)
        canvas.grid(row=0, column=0, sticky='wens')
        return canvas

    @staticmethod
    def _create_scroll(master, canvas):
        scroll = Scrollbar(master, orient='vertical', command=canvas.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        canvas.config(yscrollcommand=scroll.set, highlightthickness=0, bg='green')
        return scroll

    @staticmethod
    def _create_container(canvas):
        container = Frame(canvas)
        container.pack(fill='both', expand=True)
        container_window_sets = {
            'window': container,
            'anchor': 'nw'
        }
        container.win_id = canvas.create_window((0, 0), container_window_sets)
        return container

    def _config_container(self):
        self._canvas.config(scrollregion=self._canvas.bbox("all"))

    def _config_canvas(self, event):
        self._canvas.itemconfig(self._container.win_id, width=event.width)

    def _on_mouse_scroll(self, event):
        if Scroll.active_canvas and self._is_active():
            Scroll.active_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _is_active(self):
        (up_offset, down_offset) = self._scroll.get()
        return not (up_offset == 0.0 and down_offset == 1.0)

    def _set_canvas_active(self):
        Scroll.active_canvas = self._canvas

    def _set_canvas_inactive(self):
        if Scroll.active_canvas == self._canvas:
            Scroll.active_canvas = None

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, value):
        self._geometry = value
        if value is not None:
            value.apply(self._frame)

    @property
    def node_styles(self) -> InheritedDict:
        """Returns node styles"""
        return self._node_styles

    @property
    def container(self) -> Frame:
        return self._container

    @property
    def canvas(self) -> Canvas:
        return self._canvas

    def bind(self, event, handler):
        self._container.bind('<' + event + '>', handler)
        if 'Button-' in event:
            self._canvas.bind('<' + event + '>', handler)

    def destroy(self):
        super().destroy()
        self._frame.destroy()


def get_scroll_pipeline():
    return RenderingPipeline(steps=[
        setup_setter,
        apply_attributes,
        render_scroll_children
    ])


def setup_setter(node: Scroll, **args):
    node.attr_setter = _scroll_attr_setter


def _scroll_attr_setter(node: Scroll, key: str, value):
    if hasattr(node, key):
        setattr(node, key, value)
    elif hasattr(node.container, key):
        setattr(node.container, key, value)
    else:
        node.container.configure(**{key: value})
        if key == 'bg' or key == 'background':
            node.canvas.config(**{key: value})


def render_scroll_children(node: Scroll, **args):
    render_children(node,
                    parent_node=node,
                    node_styles=node.node_styles,
                    node_globals=node.node_globals,
                    master=node.container)
