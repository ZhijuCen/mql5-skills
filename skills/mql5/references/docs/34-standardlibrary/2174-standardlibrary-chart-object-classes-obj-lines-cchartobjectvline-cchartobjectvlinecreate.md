# Create

Creates "Vertical Line" graphical object.

```
bool  Create(
   long      chart_id,     // chart identifier
   string    name,         // object name
   int       window,       // chart window
   datetime  time          // time coordinate
   )

```

Parameters

chart_id

[in]  Chart identifier (0 – current chart).

name

[in]  A unique name of the object to create.

window

[in]  Chart window number (0 – main window).

time

[in]  Time coordinate of the anchor point.

Return Value

true - successful, false - error.
