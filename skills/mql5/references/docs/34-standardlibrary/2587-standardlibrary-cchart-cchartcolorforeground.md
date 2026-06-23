# ColorForeground (Get Method)

Gets the value of "ColorForeground" property (color of axes, scale and OHLC strings of the chart).

```
color  ColorForeground() const

```

Return Value

Value of "ColorForeground" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorForeground (Set Method)

Sets new value for "ColorForeground" property (for axes, scale, and OHLC string).

```
bool  ColorForeground(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color for axes, scale and OHLC string.

Return Value

true - successful, false - cannot change the color.
