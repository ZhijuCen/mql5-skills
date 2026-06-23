# Create

Creates CCheckBox control.

```
virtual bool  Create(
   const long    chart,      // chart ID
   const string  name,       // name
   const int     subwin,     // chart subwindow
   const int     x1,         // coordinate
   const int     y1,         // coordinate
   const int     x2,         // coordinate
   const int     y2          // coordinate
   )

```

Parameters

chart

[in]  ID of the chart, at which the control is created.

name

[in]  Unique name of the control.

subwin

[in]  Subwindow of the chart, at which the control is created.

x1

[in]  X coordinate of the upper left corner.

y1

[in]  Y coordinate of the upper left corner.

x2

[in]  X coordinate of the lower right corner.

y2

[in]  Y coordinate of the lower right corner.

Return Value

true - successful, otherwise - false.
