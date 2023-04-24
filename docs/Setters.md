# Setters

Basically setters are functions that set node or widget attributes.  

## Built-in setters

`tkviews.bind` - calls tkinter widget bind method
```xml
<Frame xmlns:bind='tkviews.bind'>
    <Button bind:Button-1="{lambda e: print('Button is clicked')}" />
</Frame>
```

`tkviews.bind_all` - calls tkinter widget bind_all method
```xml
<Frame xmlns:bind_all='tkviews.bind_all'
       bind_all:Button-1="{lambda e: print('Widget is clicked')}" />
```

`tkviews.config` - calls tkinter widget config method
```xml
<Frame xmlns:config='tkviews.config'>
    <Button config:text='Button name' />
</Frame>
```

`tkviews.call` - calls node or widget method
```xml
<Frame xmlns:call='tkviews.call'>
    <Button call:pack='{args(side="left")}' />
</Frame>
```

`tkviews.import_global` - imports and sets result to node globals
```xml
<Frame xmlns:import='tkviews.import_global'
       import:messagebox="tkinter.messagebox">
    <Button bind:Button-1="{lambda e: messagebox.showinfo('Message title', 'message content')}" />
</Frame>
```

`tkviews.set_global` - sets value to node globals
```xml
<Frame xmlns:global='tkviews.set_global'
       global:button_name="Button name">
    <Button text="{button_name}" />
</Frame>
```

`tkviews.inject_global` - injects value to node globals
```python
from injectool import add_singleton

add_singleton('default_button_name', 'Button name')
```
```xml
<Frame xmlns:inject="tkviews.inject_global"
       inject:button_name="default_button_name">
    <Button text="{button_name}" />
</Frame>
```

## Custom setter

```python
# mymodule.py
def my_setter(node: Node, key: str, value: Any):
    pass
```

and can be used in views like this:

```xml
<Label xmlns:my_setter="mymodule.my_setter" my_setter:key="value" />
```

___
[Previous](Rendering.md "Rendering") | [Next](Expressions.md "Expressions")
