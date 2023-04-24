# Binding

## Bindable

`Bindable` is a base class that can notify about its changes.  
`BindableEntity` notifies about all properties changes.
`BindableDict` notifies about values changes.

```python
from pyviews.core.bindable import BindableEntity

class BindingViewModel(BindableEntity):

    def __init__(self):
        super().__init__()
        self.value = 'value'

callback = lambda new_value, old_value: print(new_value)
view_model.observe('value', callback)
view_model.value = 'new value'
view_model.release('value', callback)
```

## Once binding

Once binding just executes expression and sets its result to node attribute.  
It doesn't create any bindings.

```xml
<Label text="once:{view_model.value}" />
```

## One way binding

One way binding executes expression and sets its result to node attribute and binds the attribute to all bindable objects in the expression.  
One way binding is used by default so it's not neccessary to indicate it explicitly.

```xml
<Label text="oneway:{view_model.value}" />
<Label text="{view_model.value}" />
```

## Two ways binding

Two way binding executes expression and sets its result to node attribute.  
It binds the attribute to all bindable objects in the expression.  
One way binding is used by default so it's not neccessary to indicate it explicitly.

```xml
<Label text="oneway:{view_model.value}" />
<Label text="{view_model.value}" />
```

## Custom binding

To use custom binding next steps should be done:

Add binding class derived from `pyviews.core.binding.Binding`
```python
class CustomBinding(Binding):
    """Binding is subscribed on tkinter Var changes"""

    def __init__(self):
        super().__init__()

    def bind(self):
        """Applies binding"""

    def destroy(self):
        """Destroys binding"""
```

Implement function to create binding from `pyviews.binding.binder.BindingContext`
```python
def create_custom_binding(bindingContext: BindingContext) -> Binding:
    """Creates binding and returns it"""
    binding = CustomBinding()
    binding.bind()
    return binding
```

Implement function that returns `True` if binding can be applied.  
`pyviews.binding.binder.BindingContext` has info about node, attribute, etc
```python
def is_suitable(bindingContext: BindingContext) -> Binding:
    """Checks binding can be applied"""
    return True
```

Add rule to `pyviews.binding.binder.Binder`
```python
@inject(binder = Binder)
def use_custom_binding(binder: Binder = In):
    """Adds tkinter variables bindings"""
    binder.add_rule('custom', create_custom_binding, is_suitable)
```

Use your custom binding
```xml
<Label text="custom:{view_model.value}" />
```

[Two ways bindings](https://github.com/eumis/tkviews/blob/dev/tkviews/widgets/binding.py) can be used as an example

___
[Previous](Expressions.md "Expressions") | [Next](Containers.md "Containers")
