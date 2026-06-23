# Vertical scale (by price and indicator readings)

Properties related to the vertical scale are set and parsed using the elements of two enumerations: ENUM_CHART_PROPERTY_INTEGER and ENUM_CHART_PROPERTY_DOUBLE. In the following table, the properties are listed along with their value type.

Some properties allow you to access not only the main window but also a subwindow, for which ChartSet and ChartGet functions should use the parameter window (0 means the main window and is the default value for the short form of ChartGet).

| Identifier | Description | Value type |
| --- | --- | --- |
| CHART_SCALEFIX | Fixed scale mode | bool |
| CHART_FIXED_MAX | Fixed maximum of the  window  subwindow or the initial maximum of the main window | double |
| CHART_FIXED_MIN | Fixed minimum of the  window  subwindow or the initial minimum of the main window | double |
| CHART_SCALEFIX_11 | Scale mode 1:1 | bool |
| CHART_SCALE_PT_PER_BAR | Scale indication mode in points per bar | bool |
| CHART_POINTS_PER_BAR | Scale value in points per bar | double |
| CHART_PRICE_MIN | Minimum values in the  window  window or subwindow (r/o) | double |
| CHART_PRICE_MAX | Maximum values in the  window  window or subwindow (r/o) | double |
| CHART_HEIGHT_IN_PIXELS | Fixed height of window or subwindow in pixels,  window  parameter required | int |
| CHART_WINDOW_YDISTANCE | Distance in pixels along the vertical Y-axis between the top frame of the  window  subwindow and the upper frame of the main chart window. (r/o) | int |

By default, charts support adaptive scale so that quotes or indicator lines fit completely vertically on a visible time period. For some applications, it is desirable to fix the scale, for which the terminal offers several modes. In them, the chart can be scrolled with the mouse or with the keys (Shift + arrow) not only left/right, but also up/down, and a slider bar appears at the right scale, using which you can quickly scroll the chart with the mouse.

The fixed mode is set by turning on the CHART_SCALEFIX flag and specifying the required maximum and minimum in the CHART_FIXED_MAX and CHART_FIXED_MIN fields (in the main window, the user will be able to move the chart up or down, due to which the CHART_FIXED_MAX and CHART_FIXED_MIN values will change synchronously, but the vertical scale will remain the same). The user will also be able to change the vertical scale by pressing the mouse button on the price scale and, without releasing it, moving it up or down. Subwindows do not provide interactive editing of the vertical scale. In this regard, we will later present an indicator SubScaler.mq5 (see [keyboard events section](/en/book/applications/events/events_keyboard)), which will allow the user to control the range of values in the subwindow using the keyboard, rather than from the settings dialog, using the fields on the Scale tab.

The CHART_SCALEFIX_11 mode provides an approximate visual equality of the sides of the square on the screen: X bars in pixels (horizontally) will be equal to X points in pixels (vertically). The equality is approximate, because the size of the pixels, as a rule, is not the same vertically and horizontally.

Finally, there is a mode for fixing the ratio of the number of points per bar, which is enabled by the CHART_SCALE_PT_PER_BAR option, and the required ratio itself is set using the CHART_POINTS_PER_BAR property. Unlike the CHART_SCALEFIX mode, the user will not be able to interactively change the scale with the mouse on the chart. In this mode, a horizontal distance of one bar will be displayed on the screen in the same ratio to the specified number of vertical points as the aspect ratio of the chart (in pixels). If the timeframes and sizes of the two charts are equal, one will look compressed in price compared to the other according to the ratio of their CHART_POINTS_PER_BAR values. Obviously, the smaller the timeframe, the smaller the range of bars, and therefore, with the same scale, small timeframes look more "flattened".

Programmatically setting the CHART_HEIGHT_IN_PIXELS property makes it impossible for the user to edit the window/subwindow size. This is often used for windows that host trading panels with a predefined set of controls (buttons, input fields, etc.). In order to remove the fixation of the size, set the value of the property to -1.

The CHART_WINDOW_YDISTANCE value is required to convert the absolute coordinates of the main chart into local coordinates of the subwindow for correct work with graphical objects. The point is that when [mouse events](/en/book/applications/events/events_mouse) occur, cursor coordinates are transferred relative to the main chart window, while the coordinates of graphical objects in the indicator subwindow are set relative to the upper left corner of the subwindow.

Let's prepare the ChartScalePrice.mq5 script for analyzing changes in vertical scales and sizes.

```
void OnStart()
{
   int flags[] =
   {
      CHART_SCALEFIX, CHART_SCALEFIX_11,
      CHART_SCALE_PT_PER_BAR, CHART_POINTS_PER_BAR,
      CHART_FIXED_MAX, CHART_FIXED_MIN,
      CHART_PRICE_MIN, CHART_PRICE_MAX,
      CHART_HEIGHT_IN_PIXELS, CHART_WINDOW_YDISTANCE
   };
   ChartModeMonitor m(flags);
   ...
}

```

It reacts to chart manipulation in the following way:

```
Initial state:
    [key] [value]   // ENUM_CHART_PROPERTY_INTEGER
[0]     6       0
[1]     7       0
[2]    10       0
[3]   107     357
[4]   110       0
    [key]  [value]  // ENUM_CHART_PROPERTY_DOUBLE
[0]    11 10.00000
[1]     8  1.13880
[2]     9  1.12330
[3]   108  1.12330
[4]   109  1.13880
// reduced the vertical size of the window
CHART_HEIGHT_IN_PIXELS 357 -> 370
CHART_HEIGHT_IN_PIXELS 370 -> 408
CHART_FIXED_MAX 1.1389 -> 1.1388
CHART_FIXED_MIN 1.1232 -> 1.1233
CHART_PRICE_MIN 1.1232 -> 1.1233
CHART_PRICE_MAX 1.1389 -> 1.1388
// reduced the horizontal scale, which increased the price range
CHART_FIXED_MAX 1.1388 -> 1.139
CHART_FIXED_MIN 1.1233 -> 1.1183
CHART_PRICE_MIN 1.1233 -> 1.1183
CHART_PRICE_MAX 1.1388 -> 1.139
CHART_FIXED_MAX 1.139 -> 1.1406
CHART_FIXED_MIN 1.1183 -> 1.1167
CHART_PRICE_MIN 1.1183 -> 1.1167
CHART_PRICE_MAX 1.139 -> 1.1406
// expand the price range using the mouse (quotes "shrink" vertically)
CHART_FIXED_MAX 1.1406 -> 1.1454
CHART_FIXED_MIN 1.1167 -> 1.1119
CHART_PRICE_MIN 1.1167 -> 1.1119
CHART_PRICE_MAX 1.1406 -> 1.1454

```
