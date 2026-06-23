# Drawing Styles

When creating [a custom indicator](/en/docs/customind), you can specify one of 18 types of graphical plotting (as displayed in the main chart window or a chart subwindow), whose values are specified in the ENUM_DRAW_TYPE enumeration.

In one custom indicator, it is permissible to use any [indicator building/drawing types](/en/docs/customind/indicators_examples). Each construction type requires specification of one to five [global arrays](/en/docs/basis/variables/global) for storing data necessary for drawing. These data arrays must be bound with indicator buffers using the [SetIndexBuffer()](/en/docs/customind/setindexbuffer) function. The type of data from [ENUM_INDEXBUFFER_TYPE](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_indexbuffer_type_enum) should be specified for each buffer.

Depending on the drawing style, you may need one to four value buffers (marked as INDICATOR_DATA). If a style admits dynamic alternation of colors (all styles contain COLOR in their names), then you'll need one more buffer of color (indicated type INDICATOR_COLOR_INDEX). The color buffers are always bound after value buffers corresponding to the style.

ENUM_DRAW_TYPE

| ID | Description | Data buffers | Color buffers |
| --- | --- | --- | --- |
| DRAW_NONE | Not drawn | 1 | 0 |
| DRAW_LINE | Line | 1 | 0 |
| DRAW_SECTION | Section | 1 | 0 |
| DRAW_HISTOGRAM | Histogram from the zero line | 1 | 0 |
| DRAW_HISTOGRAM2 | Histogram of the two indicator buffers | 2 | 0 |
| DRAW_ARROW | Drawing arrows | 1 | 0 |
| DRAW_ZIGZAG | Style Zigzag allows vertical section on the bar | 2 | 0 |
| DRAW_FILLING | Color fill between the two levels | 2 | 0 |
| DRAW_BARS | Display as a sequence of bars | 4 | 0 |
| DRAW_CANDLES | Display as a sequence of candlesticks | 4 | 0 |
| DRAW_COLOR_LINE | Multicolored line | 1 | 1 |
| DRAW_COLOR_SECTION | Multicolored section | 1 | 1 |
| DRAW_COLOR_HISTOGRAM | Multicolored histogram from the zero line | 1 | 1 |
| DRAW_COLOR_HISTOGRAM2 | Multicolored histogram of the two indicator buffers | 2 | 1 |
| DRAW_COLOR_ARROW | Drawing multicolored arrows | 1 | 1 |
| DRAW_COLOR_ZIGZAG | Multicolored ZigZag | 2 | 1 |
| DRAW_COLOR_BARS | Multicolored bars | 4 | 1 |
| DRAW_COLOR_CANDLES | Multicolored candlesticks | 4 | 1 |

To refine the display of the selected drawing type identifiers listed in ENUM_PLOT_PROPERTY are used.

For functions [PlotIndexSetInteger()](/en/docs/customind/plotindexsetinteger) and [PlotIndexGetInteger()](/en/docs/customind/plotindexgetinteger)

ENUM_PLOT_PROPERTY_INTEGER

| ID | Description | Property type |
| --- | --- | --- |
| PLOT_ARROW | Arrow code for style DRAW_ARROW | uchar |
| PLOT_ARROW_SHIFT | Vertical shift of arrows for style DRAW_ARROW | int |
| PLOT_DRAW_BEGIN | Number of initial bars without drawing and values in the DataWindow | int |
| PLOT_DRAW_TYPE | Type of graphical construction | ENUM_DRAW_TYPE |
| PLOT_SHOW_DATA | Sign of display of construction values in the DataWindow | bool |
| PLOT_SHIFT | Shift of indicator plotting along the time axis in bars | int |
| PLOT_LINE_STYLE | Drawing line style | ENUM_LINE_STYLE |
| PLOT_LINE_WIDTH | The thickness of the drawing line | int |
| PLOT_COLOR_INDEXES | The number of colors | int |
| PLOT_LINE_COLOR | The index of a buffer containing the drawing color | color       modifier = index number of colors |

For the function [PlotIndexSetDouble()](/en/docs/customind/plotindexsetdouble)

ENUM_PLOT_PROPERTY_DOUBLE

| ID | Description | Property type |
| --- | --- | --- |
| PLOT_EMPTY_VALUE | An empty value for plotting, for which there is no drawing | double |

For the function [PlotIndexSetString()](/en/docs/customind/plotindexsetstring)

ENUM_PLOT_PROPERTY_STRING

| ID | Description | Property type |
| --- | --- | --- |
| PLOT_LABEL | The name of the indicator graphical series to display in the DataWindow. When working with complex graphical styles requiring several indicator buffers for display, the names for each buffer can be specified using ";" as a separator. Sample code is shown in  DRAW_CANDLES | string |

5 styles can be used for drawing lines in custom indicators. They are valid only for the line thickness 0 or 1.

ENUM_LINE_STYLE

| ID | Description |
| --- | --- |
| STYLE_SOLID | Solid line |
| STYLE_DASH | Broken line |
| STYLE_DOT | Dotted line |
| STYLE_DASHDOT | Dash-dot line |
| STYLE_DASHDOTDOT | Dash - two points |

To set the line drawing style and the type of drawing, the [PlotIndexSetInteger()](/en/docs/customind/plotindexsetinteger) function is used. For the Fibonacci extensions the thickness and drawing style of levels can be indicated using the [ObjectSetInteger()](/en/docs/objects/objectsetinteger) function.

Example:

```
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots   1
//--- indicator buffers
double         MABuffer[];
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- Bind the Array to the indicator buffer with index 0
   SetIndexBuffer(0,MABuffer,INDICATOR_DATA);
//--- Set the line drawing
   PlotIndexSetInteger(0,PLOT_DRAW_TYPE,DRAW_LINE);
//--- Set the style line
   PlotIndexSetInteger(0,PLOT_LINE_STYLE,STYLE_DOT);
//--- Set line color
   PlotIndexSetInteger(0,PLOT_LINE_COLOR,clrRed);
//--- Set line thickness
   PlotIndexSetInteger(0,PLOT_LINE_WIDTH,1);
//--- Set labels for the line
   PlotIndexSetString(0,PLOT_LABEL,"Moving Average");
//---
  }
//+------------------------------------------------------------------+
//| Custom indicator iteration function                              |
//+------------------------------------------------------------------+
int OnCalculate(const int rates_total,
                 const int prev_calculated,
                 const datetime &time[],
                 const double &open[],
                 const double &high[],
                 const double &low[],
                 const double &close[],
                 const long &tick_volume[],
                 const long &volume[],
                 const int &spread[])
  {
//--- 
   for(int i=prev_calculated;i<rates_total;i++)
     {
      MABuffer[i]=close[i];
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }

```
