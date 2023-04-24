# Overview

Every xml node represents widget or [Node](Rendering.md#Node).
Tag namespace is interpreted as a module and tag name is used as a class name.

For example, the following XML code is [rendered](Rendering.md) a tkinter.Button widget:
```xml
<Button xmlns='tkinter' />
```

Xml attributes are used to set properties
```xml
<Button text="Button text" />
```

[Setters](Setters.md) are used for setting attributes in other ways.
The following example uses `call` setter to call `pack` method for `tkinter.Button`:
```xml
<Button
    xmlns:call='tkviews.call'
    call:pack='{args(fill="x")}'
    text="Button text" />
```

[Expressions](Expressions.md) are used to evaluate values.  
For example, the following XML code uses an expression to display the platform on which the code is running in a `tkinter.Label` widget:
```xml
<Label
    import:platform="platform"
    text="{platform.platform()}" />
```

[Bindings](Binding.md) are used to bind widget attributes to view model values.

In the following example `value` view model property is bound to `text` of `tkinter.Label`:
```python
class ViewModel(BindableEntity):

    def __init__(self):
        super().__init__()
        self.value = 'some value'
```
```xml
<Label text="{view_model.value}" />
```

___
[Previous](Quick-Start.md "Quick Start") | [Next](Rendering.md "Rendering")
