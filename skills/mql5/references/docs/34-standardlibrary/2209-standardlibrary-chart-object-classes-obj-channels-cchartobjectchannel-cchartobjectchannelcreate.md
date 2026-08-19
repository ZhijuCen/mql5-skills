# Create

Creates "Equidistant Channel" graphic object.

```
bool  Create(
   long      chart_id,     // chart identifier
   string    name,         // object name
   int       window,       // chart window
   datetime  time1,        // time coordinate of the first anchor point
   double    price1,       // price coordinate of the first anchor point
   datetime  time2,        // time coordinate of the second anchor point
   double    price2,       // price coordinate of the second anchor point
   datetime  time3,        // time coordinate of the third anchor point
   double    price3        // price coordinate of the third anchor point
   )

```

Parameters

chart_id

[in]  Chart ID (0 – current chart).

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

time3

[in]  Time coordinate of the third anchor point.

price3

[in]  Price coordinate of the third anchor point.

Return Value

true - successful, false - error.
