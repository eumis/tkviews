# Containers

Containers are nodes that provides some functionality

## Container

Used for logical grouping nodes or as placeholder for imports
```xml
<tkv:Container 
    xmlns='tkinter'
    xmlns:tkv="tkviews"
    xmlns:call='tkviews.call'
    xmlns:bind='tkviews.bind'
    xmlns:import='tkviews.import_global'
    import:messagebox="tkinter.messagebox">

    <Label text="text" />

</tkv:Container>
```

## View

Used to load markup from other file

root.xml
```xml
<tkv:View name="view" />
```

view.xml
```xml
<Label text="text" />
```

## If

`If` child nodes are rendered if condtion is `True`
```xml
<tkv:If condition="{vm.visible}">
    <Label text="text" />
</tkv:If>
```

## For

`For` repeats child nodes for every item in `items`
```xml
<tkv:For items='{vm.items}'>
    <Label text"{f'{item} with index {index}'}" />
</tkv:For>
```

## Code

`Code` runs python code
```xml
<tkv:Code>
    print('test code')
</tkv:Code>
```

___
[Previous](Binding.md "Binding")
