# ValueUpdate

Updates the specified value in the specified series.

```
 bool  ValueUpdate(
   const uint  series,  // index of the series
   const uint  pos,     // index of the element
   double      value,   // value
   )

```

Parameters

series

[in] Index of the series — the serial number of its addition, starting with 0.

pos

[in] Index of element in the series.

value

[in] New value.

Return Value

true if successful, otherwise — false.
