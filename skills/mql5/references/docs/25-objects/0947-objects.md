# Object Functions

This is the group of functions intended for working with graphic objects relating to any specified chart.

The functions defining the properties of graphical objects, as well as [ObjectCreate()](/en/docs/objects/objectcreate) and [ObjectMove()](/en/docs/objects/objectmove) operations for creating and moving objects along the chart are actually used for sending commands to the chart. If these functions are executed successfully, the command is included in the common queue of the chart events. Visual changes in the properties of graphical objects are implemented when handling the queue of the chart events.

Thus, do not expect an immediate visual update of graphical objects after calling these functions. Generally, the graphical objects on the chart are updated automatically by the terminal following the change events - a new quote arrival, resizing the chart window, etc. Use [ChartRedraw()](/en/docs/chart_operations/chartredraw) function to forcefully update the graphical objects.

| Function | Action |
| --- | --- |
| ObjectCreate | Creates an object of the specified type in a specified chart |
| ObjectName | Returns the name of an object of the corresponding type in the specified chart (specified chart subwindow) |
| ObjectDelete | Removes the object with the specified name from the specified chart (from the specified chart subwindow) |
| ObjectsDeleteAll | Removes all objects of the specified type from the specified chart (from the specified chart subwindow) |
| ObjectFind | Searches for an object with the specified ID by the name |
| ObjectGetTimeByValue | Returns the time value for the specified object price value |
| ObjectGetValueByTime | Returns the price value of an object for the specified time |
| ObjectMove | Changes the coordinates of the specified object anchor point |
| ObjectsTotal | Returns the number of objects of the specified type in the specified chart (specified chart subwindow) |
| ObjectGetDouble | Returns the double value of the corresponding object property |
| ObjectGetInteger | Returns the integer value of the corresponding object property |
| ObjectGetString | Returns the string value of the corresponding object property |
| ObjectSetDouble | Sets the value of the corresponding object property |
| ObjectSetInteger | Sets the value of the corresponding object property |
| ObjectSetString | Sets the value of the corresponding object property |
| TextSetFont | Sets the font for displaying the text using drawing methods (Arial 20 used by default) |
| TextOut | Transfers the text to the custom array (buffer) designed for creation of a graphical  resource |
| TextGetSize | Returns the string's width and height at the current  font settings |

Every graphical object should have a name unique within one [chart](/en/docs/chart_operations), including its subwindows. Changing of a name of a graphic object generates two events: event of deletion of an object with the old name, and event of creation of an object with a new name.

After an object is created or an [object property](/en/docs/constants/objectconstants/enum_object_property) is modified it is recommended to call the [ChartRedraw()](/en/docs/chart_operations/chartredraw) function, which commands the client terminal to forcibly draw a chart (and all [visible](/en/docs/constants/objectconstants/visible) objects in it).
