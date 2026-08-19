# ColorCandleBull (Get Method)

Gets the value of "ColorCandleBull" property (body color of the bullish candle).

```
color  ColorCandleBull() const

```

Return Value

Value of "ColorCandleBull" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorCandleBull (Set Method)

Sets new value for "ColorCandleBull" property.

```
bool  ColorCandleBull(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color of the bullish candle body.

Return Value

true - successful, false - cannot change the color.
