# ColorLineAsk (Get Method)

Gets the value of "ColorLineAsk" property (color of Ask line).

```
color  ColorLineAsk() const

```

Return Value

Value of "ColorLineAsk" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorLineAsk (Set Method)

Sets new value for "ColorLineAsk" property.

```
bool  ColorLineAsk(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color for Ask line.

Return Value

true - successful, false - cannot change the color.
