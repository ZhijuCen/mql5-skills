# ValueUpdate

Updates the value on the pie chart (at the specified position).

```
 bool  ValueUpdate(
   const uint    pos,    // index
   const double  value,  // value
   const string  descr,  // label
   const uint    clr,    // color
   )

```

Parameters

pos

[in] Index of the value — the serial number of its addition, starting with 0.

value

[in] Value.

descr

[in] Value label.

clr

[in] Value color.

Return Value

true if successful, otherwise — false.
