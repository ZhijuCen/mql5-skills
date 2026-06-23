# Object Properties

Graphical objects can have various properties depending on the object type. Values of object properties are set up and received by corresponding [functions for working with graphical objects](/en/docs/objects).

All objects used in technical analysis are bound to the time and price coordinates: trendline, channels, Fibonacci tools, etc. But there is a number of auxiliary objects intended to improve the user interface that are bound to the always visible part of a chart (main chart windows or indicator subwindows):

| Object | ID | X/Y | Width/Height | Date/Price | OBJPROP_CORNER | OBJPROP_ANCHOR | OBJPROP_ANGLE |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Text | OBJ_TEXT | — | — | Yes | — | Yes | Yes |
| Label | OBJ_LABEL | Yes | Yes (read only) | — | Yes | Yes | Yes |
| Button | OBJ_BUTTON | Yes | Yes | — | Yes | — | — |
| Bitmap | OBJ_BITMAP | — | Yes (read only) | Yes | — | Yes | — |
| Bitmap Label | OBJ_BITMAP_LABEL | Yes | Yes (read only) | — | Yes | Yes | — |
| Edit | OBJ_EDIT | Yes | Yes | — | Yes | — | — |
| Rectangle Label | OBJ_RECTANGLE_LABEL | Yes | Yes | — | Yes | — | — |

The following designations are used in the table:

- X/Y – coordinates of anchor points specified in pixels relative to a chart corner;
- Width/Height – objects have width and height. For "read only", the width and height values are calculated only once the object is rendered on chart;
- Date/Price – anchor point coordinates are specified using the date and price values;
- OBJPROP_CORNER – defines the chart corner relative to which the anchor point coordinates are specified. Can be one of the 4 values of the [ENUM_BASE_CORNER](/en/docs/constants/objectconstants/enum_basecorner#enum_base_corner) enumeration;
- OBJPROP_ANCHOR – defines the anchor point in object itself and can be one of the 9 values of the [ENUM_ANCHOR_POINT](/en/docs/constants/objectconstants/enum_anchorpoint#enum_anchor_point) enumeration. Coordinates in pixels are specified from this very point to selected chart corner;
- OBJPROP_ANGLE – defines the object rotation angle counterclockwise.

The functions defining the properties of graphical objects, as well as [ObjectCreate()](/en/docs/objects/objectcreate) and [ObjectMove()](/en/docs/objects/objectmove) operations for creating and moving objects along the chart are actually used for sending commands to the chart. If these functions are executed successfully, the command is included in the common queue of the chart events. Visual changes in the properties of graphical objects are implemented when handling the queue of the chart events.

Thus, do not expect an immediate visual update of graphical objects after calling these functions. Generally, the graphical objects on the chart are updated automatically by the terminal following the change events - a new quote arrival, resizing the chart window, etc. Use [ChartRedraw()](/en/docs/chart_operations/chartredraw) function to forcefully update the graphical objects.

For functions [ObjectSetInteger()](/en/docs/objects/objectsetinteger) and [ObjectGetInteger()](/en/docs/objects/objectgetinteger)

ENUM_OBJECT_PROPERTY_INTEGER

| Identifier | Description | Property Type |
| --- | --- | --- |
| OBJPROP_COLOR | Color | color |
| OBJPROP_STYLE | Style | ENUM_LINE_STYLE |
| OBJPROP_WIDTH | Line thickness | int |
| OBJPROP_BACK | Object in the background | bool |
| OBJPROP_ZORDER | Priority of a graphical object for receiving events of clicking on a chart ( CHARTEVENT_CLICK ). The default zero value is set when creating an object; the priority can be increased if necessary. When objects are placed one atop another, only one of them with the highest priority will receive the CHARTEVENT_CLICK event. | long |
| OBJPROP_FILL | Fill an object with color (for OBJ_RECTANGLE, OBJ_TRIANGLE, OBJ_ELLIPSE, OBJ_CHANNEL, OBJ_STDDEVCHANNEL, OBJ_REGRESSION) | bool |
| OBJPROP_HIDDEN | Disable the display of a graphical object in the client terminal  object list  called by the Charts \ Objects \ Object List command. This prevents accidental deletion of MQL5 program service objects by a user. In addition to hiding the object from the list, the property disables the ability to delete it using the Charts \ Objects \ Delete Last command. 
   
 The value of 'true' hides the object. By default, hidden objects are those that display calendar events and trading history, as well as those  created from an MQL5 program . Click "List all" to see them in the object list and access their properties. | bool |
| OBJPROP_SELECTED | Object is selected | bool |
| OBJPROP_READONLY | Ability to edit text in the Edit object | bool |
| OBJPROP_TYPE | Object type | ENUM_OBJECT    r/o |
| OBJPROP_TIME | Time coordinate | datetime   modifier=number of anchor point |
| OBJPROP_SELECTABLE | Object availability | bool |
| OBJPROP_CREATETIME | Time of object creation | datetime    r/o |
| OBJPROP_LEVELS | Number of levels | int |
| OBJPROP_LEVELCOLOR | Color of the line-level | color   modifier=level number |
| OBJPROP_LEVELSTYLE | Style of the line-level | ENUM_LINE_STYLE  modifier=level number |
| OBJPROP_LEVELWIDTH | Thickness of the line-level | int      modifier=level number |
| OBJPROP_ALIGN | Horizontal text alignment in the "Edit" object (OBJ_EDIT) | ENUM_ALIGN_MODE |
| OBJPROP_FONTSIZE | Font size | int |
| OBJPROP_RAY_LEFT | Ray goes to the left | bool |
| OBJPROP_RAY_RIGHT | Ray goes to the right | bool |
| OBJPROP_RAY | A vertical line goes through all the windows of a chart | bool |
| OBJPROP_ELLIPSE | Showing the full ellipse of the Fibonacci Arc object ( OBJ_FIBOARC ) | bool |
| OBJPROP_ARROWCODE | Arrow code for the Arrow object | uchar |
| OBJPROP_TIMEFRAMES | Visibility of an object at timeframes | set of flags  flags |
| OBJPROP_ANCHOR | Location of the anchor point of a graphical object | ENUM_ARROW_ANCHOR  (for OBJ_ARROW), 
 ENUM_ANCHOR_POINT  (for OBJ_LABEL , OBJ_BITMAP_LABEL  and OBJ_TEXT) |
| OBJPROP_XDISTANCE | The distance in pixels along the X axis from the binding corner (see  note ) | int |
| OBJPROP_YDISTANCE | The distance in pixels along the Y axis from the binding corner (see  note ) | int |
| OBJPROP_DIRECTION | Trend of the Gann object | ENUM_GANN_DIRECTION |
| OBJPROP_DEGREE | Level of the Elliott Wave Marking | ENUM_ELLIOT_WAVE_DEGREE |
| OBJPROP_DRAWLINES | Displaying lines for marking the Elliott Wave | bool |
| OBJPROP_STATE | Button state (pressed / depressed) | bool |
| OBJPROP_CHART_ID | ID of the "Chart" object ( OBJ_CHART ). It allows working with the properties of this object like with a normal chart using the functions described in  Chart Operations , but there some  exceptions . | long   r/o |
| OBJPROP_XSIZE | The object's width along the X axis in pixels. Specified for  OBJ_LABEL (read only), OBJ_BUTTON, OBJ_CHART, OBJ_BITMAP, OBJ_BITMAP_LABEL, OBJ_EDIT, OBJ_RECTANGLE_LABEL objects. | int |
| OBJPROP_YSIZE | The object's height along the Y axis in pixels. Specified for  OBJ_LABEL (read only), OBJ_BUTTON, OBJ_CHART, OBJ_BITMAP, OBJ_BITMAP_LABEL, OBJ_EDIT, OBJ_RECTANGLE_LABEL objects. | int |
| OBJPROP_XOFFSET | The X coordinate of the upper left corner of the  rectangular visible area  in the graphical objects "Bitmap Label" and "Bitmap" (OBJ_BITMAP_LABEL and OBJ_BITMAP). The value is set in pixels relative to the upper left corner of the original image. | int |
| OBJPROP_YOFFSET | The Y coordinate of the upper left corner of the  rectangular visible area  in the graphical objects "Bitmap Label" and "Bitmap" (OBJ_BITMAP_LABEL and OBJ_BITMAP). The value is set in pixels relative to the upper left corner of the original image. | int |
| OBJPROP_PERIOD | Timeframe for the Chart object | ENUM_TIMEFRAMES |
| OBJPROP_DATE_SCALE | Displaying the time scale for the Chart object | bool |
| OBJPROP_PRICE_SCALE | Displaying the price scale for the Chart object | bool |
| OBJPROP_CHART_SCALE | The scale for the Chart object | int   value in the range 0–5 |
| OBJPROP_BGCOLOR | The background color for  OBJ_EDIT, OBJ_BUTTON, OBJ_RECTANGLE_LABEL | color |
| OBJPROP_CORNER | The corner of the chart to link a graphical object | ENUM_BASE_CORNER |
| OBJPROP_BORDER_TYPE | Border type for the "Rectangle label" object | ENUM_BORDER_TYPE |
| OBJPROP_BORDER_COLOR | Border color for the OBJ_EDIT and OBJ_BUTTON objects | color |

When using [chart operations](/en/docs/chart_operations) for the "Chart" object ([OBJ_CHART](/en/docs/constants/objectconstants/enum_object)), the following limitations are imposed:

- It cannot be closed using [ChartClose()](/en/docs/chart_operations/chartclose);
- Symbol/period cannot be changed using the [ChartSetSymbolPeriod()](/en/docs/chart_operations/chartsetsymbolperiod) function;
- The following properties are ineffective CHART_SCALE, CHART_BRING_TO_TOP, CHART_SHOW_DATE_SCALE and CHART_SHOW_PRICE_SCALE ([ENUM_CHART_PROPERTY_INTEGER](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer)).

You can set a special mode of image display for [OBJ_BITMAP_LABEL](/en/docs/constants/objectconstants/enum_object) and [OBJ_BITMAP](/en/docs/constants/objectconstants/enum_object) objects. In this mode, only part of an original image (at which a rectangular visible area is applied) is displayed, while the rest of the image becomes invisible. The size of this area should be set using the properties OBJPROP_XSIZE and OBJPROP_YSIZE. The visible area can be "moved" only within the original image using the properties OBJPROP_XOFFSET and OBJPROP_YOFFSET.

For the fixed-sized objects: [OBJ_BUTTON](/en/docs/constants/objectconstants/enum_object/obj_button), [OBJ_RECTANGLE_LABEL](/en/docs/constants/objectconstants/enum_object/obj_rectangle_label), [OBJ_EDIT](/en/docs/constants/objectconstants/enum_object/obj_edit) and [OBJ_CHART](/en/docs/constants/objectconstants/enum_object/obj_chart), properties OBJPROP_XDISTANCE and OBJPROP_YDISTANCE set the position of the top left point of the object relative to the chart corner (OBJPROP_CORNER), from which the X and Y coordinates will be counted in pixels.

For functions [ObjectSetDouble()](/en/docs/objects/objectsetdouble) and [ObjectGetDouble()](/en/docs/objects/objectgetdouble)

ENUM_OBJECT_PROPERTY_DOUBLE

| Identifier | Description | Property Type |
| --- | --- | --- |
| OBJPROP_PRICE | Price coordinate | double    modifier=number of anchor point |
| OBJPROP_LEVELVALUE | Level value | double    modifier=level number |
| OBJPROP_SCALE | Scale (properties of Gann objects and Fibonacci Arcs) | double |
| OBJPROP_ANGLE | Angle.  For the objects with no angle specified, created from a program, the value is equal to  EMPTY_VALUE | double |
| OBJPROP_DEVIATION | Deviation for the Standard Deviation Channel | double |

For functions [ObjectSetString()](/en/docs/objects/objectsetstring) and [ObjectGetString()](/en/docs/objects/objectgetstring)

ENUM_OBJECT_PROPERTY_STRING

| Identifier | Description | Property Type |
| --- | --- | --- |
| OBJPROP_NAME | Object name | string |
| OBJPROP_TEXT | Description of the object (the text contained in the object) | string |
| OBJPROP_TOOLTIP | The text of a tooltip. If the property is not set, then the tooltip generated automatically by the terminal is shown. A tooltip can be disabled by setting the "\n" (line feed) value to it | string |
| OBJPROP_LEVELTEXT | Level description | string    modifier=level number |
| OBJPROP_FONT | Font | string |
| OBJPROP_BMPFILE | The name of BMP-file for Bitmap Label. See also  Resources | string    modifier: 0-state ON, 1-state OFF |
| OBJPROP_SYMBOL | Symbol for the Chart object | string |

For the OBJ_RECTANGLE_LABEL object ("Rectangle label") one of the three design modes can be set, to which the following values of ENUM_BORDER_TYPE correspond.

ENUM_BORDER_TYPE

| Identifier | Description |
| --- | --- |
| BORDER_FLAT | Flat form |
| BORDER_RAISED | Prominent form |
| BORDER_SUNKEN | Concave form |

For the OBJ_EDIT object ("Edit") and for the [ChartScreenShot()](/en/docs/chart_operations/chartscreenshot) function, you can specify the horizontal alignment type using the values of the ENUM_ALIGN_MODE enumeration.

ENUM_ALIGN_MODE

| Identifier | Description |
| --- | --- |
| ALIGN_LEFT | Left alignment |
| ALIGN_CENTER | Centered (only for the Edit object) |
| ALIGN_RIGHT | Right alignment |

Example:

```
#define  UP          "\x0431"
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   string label_name="my_OBJ_LABEL_object";
   if(ObjectFind(0,label_name)<0)
     {
      Print("Object ",label_name," not found. Error code = ",GetLastError());
      //--- create Label object
      ObjectCreate(0,label_name,OBJ_LABEL,0,0,0);           
      //--- set X coordinate
      ObjectSetInteger(0,label_name,OBJPROP_XDISTANCE,200);
      //--- set Y coordinate
      ObjectSetInteger(0,label_name,OBJPROP_YDISTANCE,300);
      //--- define text color
      ObjectSetInteger(0,label_name,OBJPROP_COLOR,clrWhite);
      //--- define text for object Label
      ObjectSetString(0,label_name,OBJPROP_TEXT,UP);
      //--- define font
      ObjectSetString(0,label_name,OBJPROP_FONT,"Wingdings");
      //--- define font size
      ObjectSetInteger(0,label_name,OBJPROP_FONTSIZE,10);
      //--- 45 degrees rotation clockwise
      ObjectSetDouble(0,label_name,OBJPROP_ANGLE,-45);
      //--- disable for mouse selecting
      ObjectSetInteger(0,label_name,OBJPROP_SELECTABLE,false);
      //--- draw it on the chart
      ChartRedraw(0);                                      
     }
  }

```
