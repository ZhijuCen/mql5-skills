# Create

Creates "Horizontal Line" graphical object.

```
bool  Create(
   long    chart_id,     // chart identifier
   string  name,         // object name
   long    window,       // chart window
   double  price         // price coordinate
   )

```

Parameters

chart_id

[in]  Chart identifier (0 – current chart).

name

[in]  A unique name of the object to create.

window

[in]  Chart window number (0 – main window).

price

[in]  Price coordinate of the anchor point.

Return Value

true - successful, false - error.
