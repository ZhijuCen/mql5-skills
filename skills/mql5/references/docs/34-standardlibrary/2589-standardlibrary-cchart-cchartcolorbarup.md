# ColorBarUp (Get Method)

Gets the value of "ColorBarUp" property (color for bullish bars, their shadow, and candle body outlines).

```
color  ColorBarUp() const

```

Return Value

Value of "ColorBarUp" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorBarUp (Set Method)

Sets new value for "ColorBarUp" property.

```
bool  ColorBarUp(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color for bullish bars, their shadow and candle body outlines.

Return Value

true - successful, false - cannot change the color.
