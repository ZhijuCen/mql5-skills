# ColorCandleBear (Get Method)

Gets the value of "ColorCandleBear" property (body color of the bearish candle).

```
color  ColorCandleBear() const

```

Return Value

Value of "ColorCandleBear" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorCandleBear (Set Method)

Sets new value for "ColorCandleBear" property.

```
bool  ColorCandleBear(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color of the bearish candle body.

Return Value

true - successful, false - cannot change the color.
