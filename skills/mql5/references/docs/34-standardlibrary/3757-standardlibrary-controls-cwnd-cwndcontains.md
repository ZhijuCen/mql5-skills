# Contains

Checks if the point is inside the control area of the chart.

```
bool  Contains(
   const int  x,     // X coordinate
   const int  y      // Y coordinate
   )

```

Parameters

x

[in]  X coordinate.

y

[in]  Y coordinate.

Return Value

true - the point is inside the area (including borders), otherwise - false.

# Contains

Checks if the specified control is inside the control area of the chart.

```
bool  Contains(
   const CWnd*  control      // pointer
   )  const

```

Parameters

control

[in]  Object pointer.

Return Value

true - the specified control is inside the area (including borders), otherwise - false.
