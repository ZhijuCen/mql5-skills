# Chart Properties

Identifiers of ENUM_CHART_PROPERTY enumerations are used as parameters of [functions for working with charts](/en/docs/chart_operations). The abbreviation of r/o in the "Property Type" column means that this property is read-only and cannot be changed. The w/o abbreviation in the "Property Type" column means that this property is write-only and it cannot be received. When accessing certain properties, it's necessary to specify an additional parameter-modifier (modifier), which serves to indicate the number of chart subwindows. 0 means the main window.

The functions defining the chart properties are actually used for sending change commands to the chart. If these functions are executed successfully, the command is included in the common queue of the chart events. The changes are implemented to the chart when handling the queue of the chart events.

Thus, do not expect an immediate visual update of the chart after calling these functions. Generally, the chart is updated automatically by the terminal following the change events - a new quote arrival, resizing the chart window, etc. Use [ChartRedraw()](/en/docs/chart_operations/chartredraw) function to forcefully update the chart.

For functions [ChartSetInteger()](/en/docs/chart_operations/chartsetinteger) and [ChartGetInteger()](/en/docs/chart_operations/chartgetinteger)

ENUM_CHART_PROPERTY_INTEGER

| ID | Description | Property Type |
| --- | --- | --- |
| CHART_SHOW | Price chart drawing. If false, drawing any price chart attributes is disabled and all chart border indents are eliminated, including time and price scales, quick navigation bar, Calendar event labels, trade labels, indicator and bar tooltips, indicator subwindows, volume histograms, etc. 
 Disabling the drawing is a perfect solution for creating a custom program interface using the graphical  resources . 
 The  graphical objects  are always drawn regardless of the CHART_SHOW property value. | bool |
| CHART_IS_OBJECT | Identifying "Chart" ( OBJ_CHART)  object – returns true for a graphical object. Returns false for a real chart | bool   r/o |
| CHART_BRING_TO_TOP | Show chart on top of other charts | bool |
| CHART_CONTEXT_MENU | Enabling/disabling access to the context menu using the right click. 
 When CHART_CONTEXT_MENU=false, only the chart context menu is disabled. The context menu of objects on the chart remains available. | bool  (default is true) |
| CHART_CROSSHAIR_TOOL | Enabling/disabling access to the Crosshair tool using the middle click. | bool  (default is true) |
| CHART_MOUSE_SCROLL | Scrolling the chart horizontally using the left mouse button. Vertical scrolling is also available if the value of any following properties is set to true: CHART_SCALEFIX, CHART_SCALEFIX_11 or CHART_SCALE_PT_PER_BAR 
 When CHART_MOUSE_SCROLL=false, chart scrolling with the mouse wheel is unavailable | bool |
| CHART_EVENT_MOUSE_WHEEL | Sending messages about mouse wheel events ( CHARTEVENT_MOUSE_WHEEL ) to all mql5 programs on a chart | bool  (default is true) |
| CHART_EVENT_MOUSE_MOVE | Send notifications of mouse move and mouse click events ( CHARTEVENT_MOUSE_MOVE ) to all mql5 programs on a chart | bool |
| CHART_EVENT_OBJECT_CREATE | Send a notification of an event of new object creation ( CHARTEVENT_OBJECT_CREATE ) to all mql5-programs on a chart | bool |
| CHART_EVENT_OBJECT_DELETE | Send a notification of an event of object deletion ( CHARTEVENT_OBJECT_DELETE ) to all mql5-programs on a chart | bool |
| CHART_MODE | Chart type (candlesticks, bars or line) | enum      ENUM_CHART_MODE |
| CHART_FOREGROUND | Price chart in the foreground | bool |
| CHART_SHIFT | Mode of price chart indent from the right border | bool |
| CHART_AUTOSCROLL | Mode of automatic moving to the right border of the chart | bool |
| CHART_KEYBOARD_CONTROL | Allow managing the chart using a keyboard ("Home", "End", "PageUp", "+", "-", "Up arrow", etc.). Setting CHART_KEYBOARD_CONTROL to false disables chart scrolling and scaling while leaving intact the ability to receive the keys pressing events in  OnChartEvent() . | bool |
| CHART_QUICK_NAVIGATION | Allow the chart to intercept Space and Enter key strokes to activate the quick navigation bar. The quick navigation bar automatically appears at the bottom of the chart after double-clicking the mouse or pressing Space/Enter. It allows you to quickly change a symbol, timeframe and first visible bar date. | bool |
| CHART_SCALE | Scale | int        from 0 to 5 |
| CHART_SCALEFIX | Fixed scale mode | bool |
| CHART_SCALEFIX_11 | Scale 1:1 mode | bool |
| CHART_SCALE_PT_PER_BAR | Scale to be specified in points per bar | bool |
| CHART_SHOW_TICKER | Display a symbol ticker in the upper left corner. Setting CHART_SHOW_TICKER to 'false' also sets  CHART_SHOW_OHLC  to 'false' and disables OHLC | bool |
| CHART_SHOW_OHLC | Display OHLC values in the upper left corner. Setting CHART_SHOW_OHLC to 'true' also sets  CHART_SHOW_TICKER  to 'true' and enables the ticker | bool |
| CHART_SHOW_BID_LINE | Display Bid values as a horizontal line in a chart | bool |
| CHART_SHOW_ASK_LINE | Display Ask values as a horizontal line in a chart | bool |
| CHART_SHOW_LAST_LINE | Display Last values as a horizontal line in a chart | bool |
| CHART_SHOW_PERIOD_SEP | Display vertical separators between adjacent periods | bool |
| CHART_SHOW_GRID | Display grid in the chart | bool |
| CHART_SHOW_VOLUMES | Display volume in the chart | enum      ENUM_CHART_VOLUME_MODE |
| CHART_SHOW_OBJECT_DESCR | Display textual descriptions of objects (not available for all objects) | bool |
| CHART_SHOW_TRADE_HISTORY | Display trades from the trading history as entry/exit arrows on a chart. See the " Show trading history " option descriptions in the platform settings. | bool |
| CHART_VISIBLE_BARS | The number of bars on the chart that can be displayed | int r/o |
| CHART_WINDOWS_TOTAL | The total number of chart windows, including indicator subwindows | int r/o |
| CHART_WINDOW_IS_VISIBLE | Visibility of subwindows | bool r/o   modifier - subwindow number |
| CHART_WINDOW_HANDLE | Chart window handle (HWND) | int r/o |
| CHART_WINDOW_YDISTANCE | The distance between the upper frame of the indicator subwindow and the upper frame of the main chart window, along the vertical Y axis, in pixels. In case of a mouse event, the cursor coordinates are passed in terms of the coordinates of the main chart window, while the coordinates of graphical objects in an indicator subwindow are set relative to the upper left corner of the subwindow.  
 The value is required for converting the absolute coordinates of the main chart to the local coordinates of a subwindow for correct work with the graphical objects, whose coordinates are set relative to  the upper left corner of the subwindow frame. | int r/o     modifier - subwindow number |
| CHART_FIRST_VISIBLE_BAR | Number of the first visible bar in the chart. Indexing of bars is the same as for  timeseries . | int r/o |
| CHART_WIDTH_IN_BARS | Chart width in bars | int r/o |
| CHART_WIDTH_IN_PIXELS | Chart width in pixels | int r/o |
| CHART_HEIGHT_IN_PIXELS | Chart height in pixels | int      modifier - subwindow number |
| CHART_COLOR_BACKGROUND | Chart background color | color |
| CHART_COLOR_FOREGROUND | Color of axes, scales and OHLC line | color |
| CHART_COLOR_GRID | Grid color | color |
| CHART_COLOR_VOLUME | Color of volumes and position opening levels | color |
| CHART_COLOR_CHART_UP | Color for the up bar, shadows and body borders of bull candlesticks | color |
| CHART_COLOR_CHART_DOWN | Color for the down bar, shadows and body borders of bear candlesticks | color |
| CHART_COLOR_CHART_LINE | Line chart color and color of "Doji" Japanese candlesticks | color |
| CHART_COLOR_CANDLE_BULL | Body color of a bull candlestick | color |
| CHART_COLOR_CANDLE_BEAR | Body color of a bear candlestick | color |
| CHART_COLOR_BID | Bid price level color | color |
| CHART_COLOR_ASK | Ask price level color | color |
| CHART_COLOR_LAST | Line color of the last executed deal price (Last) | color |
| CHART_COLOR_STOP_LEVEL | Color of stop order levels (Stop Loss and Take Profit) | color |
| CHART_SHOW_TRADE_LEVELS | Displaying trade levels in the chart (levels of open positions, Stop Loss, Take Profit and pending orders) | bool |
| CHART_DRAG_TRADE_LEVELS | Permission to drag trading levels on a chart with a mouse. The drag mode is enabled by default (true value) | bool |
| CHART_SHOW_DATE_SCALE | Showing the time scale on a chart | bool |
| CHART_SHOW_PRICE_SCALE | Showing the price scale on a chart | bool |
| CHART_SHOW_ONE_CLICK | Showing the  "One click trading"  panel on a chart | bool |
| CHART_IS_MAXIMIZED | Chart window is maximized | bool  r/o |
| CHART_IS_MINIMIZED | Chart window is minimized | bool  r/o |
| CHART_IS_DOCKED | The chart window is docked. If set to  false , the chart can be dragged outside the terminal area | bool |
| CHART_FLOAT_LEFT | The left coordinate of the undocked chart window relative to the virtual screen | int |
| CHART_FLOAT_TOP | The top coordinate of the undocked chart window relative to the virtual screen | int |
| CHART_FLOAT_RIGHT | The right coordinate of the undocked chart window relative to the virtual screen | int |
| CHART_FLOAT_BOTTOM | The bottom coordinate of the undocked chart window relative to the virtual screen | int |

For functions [ChartSetDouble()](/en/docs/chart_operations/chartsetdouble) and [ChartGetDouble()](/en/docs/chart_operations/chartgetdouble)

ENUM_CHART_PROPERTY_DOUBLE

| ID | Description | Property Type |
| --- | --- | --- |
| CHART_SHIFT_SIZE | The size of the zero bar indent from the right border in percents | double  (from 10 to 50 percents) |
| CHART_FIXED_POSITION | Chart fixed position from the left border in percent value. Chart fixed position is marked by a small gray triangle on the horizontal time axis. It is displayed only if the automatic chart scrolling to the right on tick incoming is disabled (see CHART_AUTOSCROLL property). The bar on a fixed position remains in the same place when zooming in and out. | double |
| CHART_FIXED_MAX | Fixed  chart maximum | double |
| CHART_FIXED_MIN | Fixed  chart minimum | double |
| CHART_POINTS_PER_BAR | Scale in points per bar | double |
| CHART_PRICE_MIN | Chart minimum | double r/o   modifier - subwindow number |
| CHART_PRICE_MAX | Chart maximum | double r/o   modifier - subwindow number |

For functions [ChartSetString()](/en/docs/chart_operations/chartsetstring) and [ChartGetString()](/en/docs/chart_operations/chartgetstring)

ENUM_CHART_PROPERTY_STRING

| ID | Description | Property Type |
| --- | --- | --- |
| CHART_COMMENT | Text of a comment in a chart | string |
| CHART_EXPERT_NAME | The name of the Expert Advisor running on the chart with the specified chart_id | string r/o |
| CHART_SCRIPT_NAME | The name of the script running on the chart with the specified chart_id | string r/o |

Example:

```
   int chartMode=ChartGetInteger(0,CHART_MODE);
   switch(chartMode)
     {
      case(CHART_BARS):    Print("CHART_BARS");   break;
      case(CHART_CANDLES): Print("CHART_CANDLES");break;
      default:Print("CHART_LINE");
     }
   bool shifted=ChartGetInteger(0,CHART_SHIFT);
   if(shifted) Print("CHART_SHIFT = true");
   else Print("CHART_SHIFT = false");
   bool autoscroll=ChartGetInteger(0,CHART_AUTOSCROLL);
   if(autoscroll) Print("CHART_AUTOSCROLL = true");
   else Print("CHART_AUTOSCROLL = false");
   int chartHandle=ChartGetInteger(0,CHART_WINDOW_HANDLE);
   Print("CHART_WINDOW_HANDLE = ",chartHandle);
   int windows=ChartGetInteger(0,CHART_WINDOWS_TOTAL);
   Print("CHART_WINDOWS_TOTAL = ",windows);
   if(windows>1)
     {
      for(int i=0;i<windows;i++)
        {
         int height=ChartGetInteger(0,CHART_HEIGHT_IN_PIXELS,i);
         double priceMin=ChartGetDouble(0,CHART_PRICE_MIN,i);
         double priceMax=ChartGetDouble(0,CHART_PRICE_MAX,i);
         Print(i+": CHART_HEIGHT_IN_PIXELS = ",height," pixels");
         Print(i+": CHART_PRICE_MIN = ",priceMin);
         Print(i+": CHART_PRICE_MAX = ",priceMax);
        }
     }

```

See also

[Examples of Working with the Chart](/en/docs/constants/chartconstants/charts_samples)
