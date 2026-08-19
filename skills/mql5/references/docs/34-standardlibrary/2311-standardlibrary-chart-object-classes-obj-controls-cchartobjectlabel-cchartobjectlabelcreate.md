# Create

Creates "Label" graphical object.

```
bool  Create(
   long    chart_id,     // chart identifier
   string  name,         // object name
   int     window,       // chart window
   int     X,            // X coordinate
   int     Y             // Y coordinate
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

Return Value

true - successful, false - error.
