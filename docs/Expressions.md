# Expressions

Expressions can be used in attribute values to specify dynamic values.
An expression can be any valid Python expression that can be evaluated at runtime.
Expressions are enclosed in curly braces {} within an attribute value.

Here's an example of using an expression in the `text` attribute of a `Label` node:

```xml
<Label text="{f'{len(items)} items'}" />
```

Expressions use [node globals](Rendering.md#Node-globals) as python expression globals.

___
[Previous](Setters.md "Setters") | [Next](Binding.md "Binding")
