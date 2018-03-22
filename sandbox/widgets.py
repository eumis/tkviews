from tkinter import Frame, Canvas, Scrollbar
from pyviews.core.xml import XmlNode
from pyviews.core.node import Node
from tkviews.node import TkRenderArgs

class Scroll(Node):
    def __init__(self, master, xml_node: XmlNode, parent_context=None):
        super().__init__(xml_node, parent_context)
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

    def _create_scroll_frame(self, master):
        frame = Frame(master)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return frame


    def _create_canvas(self, master):
        canvas = Canvas(master)
        canvas.grid(row=0, column=0, sticky='wens')
        return canvas

    def _create_scroll(self, master, canvas):
        scroll = Scrollbar(master, orient='vertical', command=canvas.yview)
        scroll.grid(row=0, column=1, sticky='ns')
        canvas.config(yscrollcommand=scroll.set, highlightthickness=0, bg='green')
        return scroll

    def _create_container(self, canvas):
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
            Scroll.active_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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

    def set_attr(self, name, value):
        if hasattr(self, name):
            setattr(self, name, value)
        elif hasattr(self._container, name):
            setattr(self._container, name, value)
        else:
            self._container.configure(**{name: value})
            if name == 'bg' or name == 'background':
                self._canvas.config(**{name: value})

    def bind(self, event, handler):
        self._container.bind('<'+event+'>', handler)
        if 'Button-' in event:
            self._canvas.bind('<'+event+'>', handler)

    def get_render_args(self, xml_node):
        return TkRenderArgs(xml_node, self, self._container)

    def destroy(self):
        super().destroy()
        self._frame.destroy()
