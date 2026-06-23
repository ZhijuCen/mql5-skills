# Tooltip (Get Method)

Gets the tooltip text of a graphical object.

```
string  Tooltip() const

```

Return Value

The text of a tooltip of the graphical object attached to an instance of the class. If there is no attached object, it returns NULL.

# Tooltip (Set Method)

Sets the text of the tooltip of a graphical object.

```
bool  Tooltip(
   string  new_tooltip      // new text of a tooltip
   )

```

Parameters

new_tooltip

[in]  New text of a graphical object tooltip.

Return Value

true – success, false - cannot change the tooltip.

Note:

If the property is not set, then the tooltip generated automatically by the terminal is shown. A tooltip can be disabled by setting the "\n" (line feed) value.
