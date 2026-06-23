# ColorBarDown (Get Method)

Gets the value of "ColorBarDown" property (color for bearish bars, their shadow, and candle body outlines).

```
color  ColorBarDown() const

```

Return Value

Value of "ColorBarDown" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorBarDown (Set Method)

Sets new value for "ColorBarDown" property.

```
bool  ColorBarDown(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color for bearish bars, their shadow, and candle body outlines.

Return Value

true - successful, false - cannot change the color.
