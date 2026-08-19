# Z_Order (Get Method)

Gets the graphical object priority for receiving an event of mouse clicking on a chart ([CHARTEVENT_CLICK](/en/docs/constants/chartconstants/enum_chartevents)).

```
long  Z_Order() const

```

Return Value

Priority of a graphical object, attached to the class instance. If there is no object attached, it returns 0.

# Z_Order (Set Method)

Sets the graphical object priority for receiving an event of mouse clicking on a chart ([CHARTEVENT_CLICK](/en/docs/constants/chartconstants/enum_chartevents)).

```
bool  Z_Order(
   long  value      // graphical object priority
   )

```

Parameters

value

[in]  New value of priority of a graphical object for receiving the event [CHARTEVENT_CLICK](/en/docs/constants/chartconstants/enum_chartevents).

Return Value

true - success, false - cannot change the priority.

Note

Z_Order property manages a priority when handling clicks on graphical objects. By setting the value greater than 0 (default value), you can increase the object priority when handling mouse clicks.
