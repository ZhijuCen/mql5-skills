# The Chart Corner to Which an Object Is Attached

There is a number of [graphical objects](/en/docs/constants/objectconstants/enum_object) for which you can set a chart corner, relative to which the coordinates are specified in pixels. These are the following types of objects (in brackets object type identifiers are specified):

- Label (OBJ_LABEL);
- Button (OBJ_BUTTON);
- Bitmap Label (OBJ_BITMAP_LABEL);
- Edit (OBJ_EDIT).

- Rectangle Label (OBJ_RECTANGLE_LABEL);

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

In order to specify the chart corner, from which X and Y coordinates will be measured in pixels, use [ObjectSetInteger](/en/docs/objects/objectsetinteger)(chartID, name, [OBJPROP_CORNER](/en/docs/constants/objectconstants/enum_object_property), chart_corner), where:

- chartID - chart identifier;
- name –  name of a graphical object;
- OBJPROP_CORNER – property ID to specify the corner for binding;
- chart_corner – the desired chart corner, can be one of the values of the ENUM_BASE_CORNER enumeration.

ENUM_BASE_CORNER

| ID | Description |
| --- | --- |
| CORNER_LEFT_UPPER | Center of coordinates is in the upper left corner of the chart |
| CORNER_LEFT_LOWER | Center of coordinates is in the lower left corner of the chart |
| CORNER_RIGHT_LOWER | Center of coordinates is in the lower right corner of the chart |
| CORNER_RIGHT_UPPER | Center of coordinates is in the upper right corner of the chart |

Example:

```
void CreateLabel(long   chart_id,
                 string name,
                 int    chart_corner,
                 int    anchor_point,
                 string text_label,
                 int    x_ord,
                 int    y_ord)
  {
//---
   if(ObjectCreate(chart_id,name,OBJ_LABEL,0,0,0))
     {
      ObjectSetInteger(chart_id,name,OBJPROP_CORNER,chart_corner);
      ObjectSetInteger(chart_id,name,OBJPROP_ANCHOR,anchor_point);
      ObjectSetInteger(chart_id,name,OBJPROP_XDISTANCE,x_ord);
      ObjectSetInteger(chart_id,name,OBJPROP_YDISTANCE,y_ord);
      ObjectSetString(chart_id,name,OBJPROP_TEXT,text_label);
     }
   else
      Print("Failed to create the object OBJ_LABEL ",name,", Error code = ", GetLastError());
  }
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---
   int height=(int)ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,0);
   int width=(int)ChartGetInteger(0,CHART_WIDTH_IN_PIXELS,0);
   string arrows[4]={"LEFT_UPPER","RIGHT_UPPER","RIGHT_LOWER","LEFT_LOWER"};
   CreateLabel(0,arrows[0],CORNER_LEFT_UPPER,ANCHOR_LEFT_UPPER,arrows[0],50,50);
   CreateLabel(0,arrows[1],CORNER_RIGHT_UPPER,ANCHOR_RIGHT_UPPER,arrows[1],50,50);
   CreateLabel(0,arrows[2],CORNER_RIGHT_LOWER,ANCHOR_RIGHT_LOWER,arrows[2],50,50);
   CreateLabel(0,arrows[3],CORNER_LEFT_LOWER,ANCHOR_LEFT_LOWER,arrows[3],50,50);
  }

```
