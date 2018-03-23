'''Wrapper under tkinter widgets'''

from tkinter import BooleanVar, IntVar
from pyviews.core.xml import XmlNode
from tkviews.node import WidgetNode

class CheckbuttonNode(WidgetNode):
    '''Wrapper under Checkbutton'''
    def __init__(self, widget, xml_node: XmlNode, parent_context=None):
        super().__init__(widget, xml_node, parent_context)
        self._variable = None
        self.variable = BooleanVar()

    @property
    def variable(self):
        '''Variable linked to Checkbutton'''
        return self._variable

    @variable.setter
    def variable(self, var):
        self._variable = var
        self.widget.config(variable=var)

    @property
    def value(self):
        '''Value from variable'''
        return self.variable.get()

    @value.setter
    def value(self, checked):
        self.variable.set(checked)


class RadiobuttonNode(WidgetNode):
    '''Wrapper under Checkbutton'''
    def __init__(self, widget, xml_node: XmlNode, parent_context=None):
        super().__init__(widget, xml_node, parent_context)
        self._variable = None
        self.variable = IntVar()

    @property
    def variable(self):
        '''Variable linked to Checkbutton'''
        return self._variable

    @variable.setter
    def variable(self, var):
        self._variable = var
        self.widget.config(variable=var)

    @property
    def selected_value(self):
        '''Value from variable'''
        return self.variable.get()

    @selected_value.setter
    def selected_value(self, checked):
        self.variable.set(checked)
