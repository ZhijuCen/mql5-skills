# ColorChartLine (Get Method)

Gets the value of "ColorChartLine" property (color for line chart and Doji candles).

```
color  ColorChartLine() const

```

Return Value

Value of "ColorChartLine" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorChartLine (Set Method)

Sets new value for "ColorChartLine" property.

```
bool  ColorChartLine(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color of the chart lines and Doji candles.

Return Value

true - successful, false - cannot change the color.
