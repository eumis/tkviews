from unittest.mock import Mock

from pytest import mark
from pyviews.core.rendering import Node, NodeGlobals
from pyviews.core.xml import XmlAttr
from pyviews.setters import call

from tkviews import bind
from tkviews.core import render_attribute


@mark.parametrize('node_globals, xml_attr, setter, value', [
    ({}, XmlAttr('', 'value', 'tkviews.bind'), bind, 'value'),
    ({'value': 1}, XmlAttr('', '{1 + value}', 'pyviews.setters.call'), call, 2)
]) # yapf: disable
def test_render_attribute(node_globals, xml_attr, setter, value):
    """should return setter and value"""
    node = Node(Mock(), node_globals = NodeGlobals(node_globals))

    actual = render_attribute(node, xml_attr)

    assert actual == (setter, value)
