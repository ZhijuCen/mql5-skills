# Applying directives to customize plots

So far, we have been customizing graphic plots using PlotIndexSetInteger function calls. MQL5 allows you to do the same using #property preprocessor directives. The main difference between these two methods is that the directives are processed at compile time and the properties described with them are read from the executable file during loading, even before the handler OnInit is executed (if it exists). That is, the directives provide some default values which may be used as is if you don't need to change them.

On the other hand, the PlotIndexSetInteger function call allows you to change properties on the go, during program execution. Changing properties dynamically using functions allows you to create more flexible scenarios for using the indicator. The directives and the relevant PlotIndexSetInteger function calls are shown in the table below.

| Directives | Function | Description |
| --- | --- | --- |
| indicator_colorN | PlotIndexSetInteger(N-1, PLOT_LINE_COLOR, color) | Line color for plotting |
| indicator_styleN | PlotIndexSetInteger(N-1, PLOT_LINE_STYLE, type) | Drawing style from the ENUM_LINE_STYLE enumeration |
| indicator_typeN | PlotIndexSetInteger(N-1, PLOT_DRAW_TYPE, type) | Drawing type from the ENUM_DRAW_TYPE enumeration |
| indicator_widthN | PlotIndexSetInteger(N-1, PLOT_LINE_WIDTH, width) | Line thickness in pixels (1 - 5) |

Please note that the numbering of plots in directives starts from 1, while in functions it starts from 0. For example, the directive #property indicator_type1 DRAW_ZIGZAG is equivalent to calling PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ZIGZAG).

It is also worth noting that by using the function, you can set many more properties than through directives: the [ENUM_PLOT_PROPERTY_INTEGER](/en/book/applications/indicators_make/indicators_plotindexsetinteger) enumeration provides ten elements.

The properties described by the directives are available (visible and can be edited by the user) in the indicator settings dialog even when it is placed on the chart for the first time. In particular, this includes the thickness, color, and style of the lines (tab Colors), the number and placement of levels (tab Levels). The same properties set by functions (and if they do not have default values in directives) appear in the dialog only the second and subsequent times.

Let's adjust the IndHighLowClose.mq5 indicator to use directives. The new version is in the file IndPropHighLowClose.mq5. The use of directives simplifies the OnInit handler; OnCalculate does not change.

```
#property indicator_chart_window
#property indicator_buffers 3
#property indicator_plots 2
   
// High-Low histogram rendering settings (change index 0 to 1 in the directive)
#property indicator_type1   DRAW_HISTOGRAM2
#property indicator_style1  STYLE_SOLID // by default, can be omitted
#property indicator_color1  clrBlue
#property indicator_width1  5
   
// close line drawing settings (change index 1 to 2 in the directive)
#property indicator_type2   DRAW_LINE
#property indicator_style2  STYLE_SOLID // by default, can be omitted
#property indicator_color2  clrRed
#property indicator_width2  2
   
double highs[];
double lows[];
double closes[];
   
int OnInit()
{
   // arrays for buffers for 3 price types
   SetIndexBuffer(0, highs);
   SetIndexBuffer(1, lows);
   SetIndexBuffer(2, closes);
   
   return INIT_SUCCEEDED;
}

```

The new indicator looks absolutely the same as the old one.
