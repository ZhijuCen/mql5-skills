# Create

Creates "Linear Regression Channel" graphical object.

```
bool  Create(
   long      chart_id,     // chart identifier
   string    name,         // object name
   long      window,       // chart window
   datetime  time1,        // first time coordinate
   datetime  time2         // second time coordinate
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

time2

[in]  Time coordinate of the second anchor point.

Return Value

true - successful, false - error.
