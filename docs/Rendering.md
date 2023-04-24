# Rendering

## Node

tkviews rendering is a process of parsing xml and creating Node object.

For example:
```xml
<Button text="Button text" />
```
is equivalent to
```python
button = Button()
node = WidgetNode(button)
node.instance.text = "Button text"
```

## Custom widget

For example you have custom widget
```python
# module custom.py

class CustomWidget(Frame)
    pass
```

You need to setup [rendering pipeline](#Rendering-pipeline)
```python
from pyviews.rendering.pipeline import use_pipeline
from tkviews.widgets import get_widget_pipeline

use_pipeline(get_widget_pipeline(), 'custom.CustomWidget')
```

Now you can use your widget in view
```xml
<custom:CustomWidget xmlns:custom="custom" />
```

## Rendering pipeline

Rendering pipeline is class containing pipes - functions called one by one for node during rendering.  
Here is example of pipe:
```python
def custom_pipe(node: WidgetNode, context: TkRenderingContext):
    """Do some things"""
```

So you can build custom rendering pipeline:
```python
def get_custom_widget_pipeline() -> RenderingPipeline:
    """Returns setup for widget"""
    return RenderingPipeline(pipes=[
        setup_widget_setter,
        setup_widget_destroy,
        apply_attributes,
        apply_text,
        custom_pipe,
        add_to_panedwindow,
        render_widget_children
    ], create_node=_create_widget_node, name='custom widget pipeline')
```

And use your custom pipeline for all widgets from tkinter module
```python
use_pipeline(get_custom_widget_pipeline(), 'tkinter')
use_pipeline(get_custom_widget_pipeline(), 'tkinter.ttk')
```

## Node globals

Node globals is a dictionary with values, which are used as globals for [Expressions](Expressions.md).

Parent globals are available in child nodes. For example

```xml
<Frame global:view_model="{ViewModel()}">
    <Label text="{view_model.value}" />
</Frame>
```

In this example, the `Frame` node defines a `view_model` value in the globals dictionary.
This value is then accessed in the `Label` node using an expression ({view_model.value}).

___
[Previous](Overview.md "Overview") | [Next](Setters.md "Setters")
