Expressions can be used in attribute values to specify dynamic values.
An expression can be any valid Python expression that can be evaluated at runtime.
Expressions are enclosed in curly braces {} within an attribute value.

Here's an example of using an expression in the `text` attribute of a `Label` node:

```xml
<Label text="{f'{len(items)} items'}" />
```

Attribute value cannot be partially expression. For example

```xml
<Label text="{len(items)} items" />
```

Here label text will be interpreted as plain text: `"{len(items)} items"`

Expressions use [node globals](Rendering#Node-globals) as python expression globals.
