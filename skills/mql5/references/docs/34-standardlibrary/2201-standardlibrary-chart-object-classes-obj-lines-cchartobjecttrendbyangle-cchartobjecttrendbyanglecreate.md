# Create

Creates "Trend Line by Angle" graphical object.

```
bool  Create(
   long      chart_id,     // chart identifier
   string    name,         // object name
   long      window,       // chart window
   datetime  time1,        // 1st time coordinate
   double    price1,       // 1st price coordinate
   datetime  time2,        // 2nd time coordinate
   double    price2        // 2nd price coordinate
   )

```

Parameters

chart_id

[in]  Chart identifier (0 – current chart).

name

[in]  A unique name of the object to create.

window

[in]  Chart window number (0 – main window).

time1

[in]  Time coordinate of the first anchor point.

price1

[in]  Price coordinate of the first anchor point.

time2

[in]  Time coordinate of the second anchor point.

price2

[in]  Price coordinate of the second anchor point.

Return Value

true - successful, false - error.
