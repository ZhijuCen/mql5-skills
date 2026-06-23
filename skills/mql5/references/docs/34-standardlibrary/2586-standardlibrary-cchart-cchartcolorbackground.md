# ColorBackground (Get Method)

Gets the value of "ColorBackground" property (background color of the chart).

```
color  ColorBackground() const

```

Return Value

Value of "ColorBackground" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorBackground (Set Method)

Sets new value for "ColorBackground" property.

```
bool  ColorBackground(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New background color.

Return Value

true - successful, false - cannot change the color.
