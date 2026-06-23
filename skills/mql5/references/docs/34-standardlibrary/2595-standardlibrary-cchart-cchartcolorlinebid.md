# ColorLineBid (Get Method)

Gets the value of "ColorLineBid" property (color of Bid line).

```
color  ColorLineBid() const

```

Return Value

Value of "ColorLineBid" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorLineBid (Set Method)

Sets new value for "ColorLineBid" property.

```
bool  ColorLineBid(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color for Bid line.

Return Value

true - successful, false - cannot change the color.
