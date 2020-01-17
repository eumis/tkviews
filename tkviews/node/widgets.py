# from tkviews.widgets import WidgetNode
# from tkinter import Widget, BooleanVar, StringVar, IntVar
# from pyviews.core import XmlNode, InheritedDict
#
#
# class EntryNode(WidgetNode):
#     """Wrapper under Entry"""
#
#     def __init__(self, widget: Widget, xml_node: XmlNode,
#                  node_globals: InheritedDict = None, node_styles: InheritedDict = None):
#         super().__init__(widget, xml_node, node_globals=node_globals, node_styles=node_styles)
#         self._textvariable = None
#         self.textvariable = StringVar()
#
#     @property
#     def textvariable(self):
#         """Variable linked to Checkbutton"""
#         return self._textvariable
#
#     @textvariable.setter
#     def textvariable(self, var):
#         self._textvariable = var
#         self.instance.config(textvariable=var)
#
#     @property
#     def text(self):
#         """Value from variable"""
#         return self.textvariable.get()
#
#     @text.setter
#     def text(self, checked):
#         self.textvariable.set(checked)
#
#
# class CheckbuttonNode(WidgetNode):
#     """Wrapper under Checkbutton"""
#
#     def __init__(self, widget: Widget, xml_node: XmlNode,
#                  node_globals: InheritedDict = None, node_styles: InheritedDict = None):
#         super().__init__(widget, xml_node, node_globals=node_globals, node_styles=node_styles)
#         self._variable = None
#         self.variable = BooleanVar()
#
#     @property
#     def variable(self):
#         """Variable linked to Checkbutton"""
#         return self._variable
#
#     @variable.setter
#     def variable(self, var):
#         self._variable = var
#         self.instance.config(variable=var)
#
#     @property
#     def value(self):
#         """Value from variable"""
#         return self.variable.get()
#
#     @value.setter
#     def value(self, checked):
#         self.variable.set(checked)
#
#
# class RadiobuttonNode(WidgetNode):
#     """Wrapper under Checkbutton"""
#
#     def __init__(self, widget: Widget, xml_node: XmlNode,
#                  node_globals: InheritedDict = None, node_styles: InheritedDict = None):
#         super().__init__(widget, xml_node, node_globals=node_globals, node_styles=node_styles)
#         self._variable = None
#         self.variable = IntVar()
#
#     @property
#     def variable(self):
#         """Variable linked to Checkbutton"""
#         return self._variable
#
#     @variable.setter
#     def variable(self, var):
#         self._variable = var
#         self.instance.config(variable=var)
#
#     @property
#     def selected_value(self):
#         """Value from variable"""
#         return self.variable.get()
#
#     @selected_value.setter
#     def selected_value(self, checked):
#         self.variable.set(checked)
