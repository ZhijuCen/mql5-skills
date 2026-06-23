# Create

Creates the "CChartObjectRectLabel" graphic object.

```
bool  Create(
   long    chart_id,     // chart ID
   string  name,         // object name
   int     window,       // chart window 
   int     X,            // X coordinate
   int     Y,            // Y coordinate
   int     sizeX,        // horizontal size
   int     sizeY         // vertical size
   )

```

Parameters

chart_id

[in]  Chart identifier (0 – current chart).

name

[in]  A unique name of the object to create.

window

[in]  Chart window number (0 – main window).

X

[in]  X coordinate.

Y

[in]  Y coordinate.

sizeX

[in]  Horizontal size.

sizeY

[in]  Vertical size.

Return Value

true - successful, false - error.
