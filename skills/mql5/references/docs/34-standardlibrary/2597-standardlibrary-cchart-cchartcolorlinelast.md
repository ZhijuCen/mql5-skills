# ColorLineLast (Get Method)

Gets the value of "ColorLineLast" property (color of the last deal price line).

```
color  ColorLineLast() const

```

Return Value

Value of "ColorLineLast" property of the chart assigned to the class instance. If there is no chart assigned, it returns [CLR_NONE](/en/docs/constants/namedconstants/otherconstants).

# ColorLineLast (Set Method)

Sets new value for "ColorLineLast" property.

```
bool  ColorLineLast(
   color  new_color      // color
   )

```

Parameters

new_color

[in]  New color of the last deal price line.

Return Value

true - successful, false - cannot change the color.
