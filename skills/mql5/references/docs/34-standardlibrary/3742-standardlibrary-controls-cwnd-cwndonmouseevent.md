# OnMouseEvent

Mouse event handler (the [CHARTEVENT_MOUSE_MOVE](/en/docs/constants/chartconstants/enum_chartevents) chart event).

```
virtual bool  OnMouseEvent(
   const int  x,         // x coordinate
   const int  y,         // y coordinate
   const int  flags      // flags
   )

```

Parameters

x

[in]  X coordinate of the mouse cursor relative to the upper-left corner of the chart.

y

[in]  Y coordinate of the mouse cursor relative to the upper-left corner of the chart.

flags

[in]  Flag of mouse buttons states.

Return Value

true - event has been processed, otherwise - false.
