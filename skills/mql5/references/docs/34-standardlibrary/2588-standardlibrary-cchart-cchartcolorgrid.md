# ColorGrid (Get Method)

Gets the value of "ColorGrid" property (color of the grid).

```
color  ColorGrid() const

```

Return Value

Value of "ColorGrid" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorGrid (Set Method)

Sets new value for "ColorGrid" property.

```
bool  ColorGrid(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New grid color.

Return Value

true - successful, false - cannot change the color.
