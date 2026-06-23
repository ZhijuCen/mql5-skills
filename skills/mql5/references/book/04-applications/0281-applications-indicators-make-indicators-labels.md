# Setting plot names

In the previous examples within this chapter, indicator buffers in the Data Window were designated by the name of the indicator itself. This is not informative. The MQL5 API provides the ability to set a custom name for each buffer. This can be done in two ways which we already know: by using the #property directive and by calling the special PlotIndexSetString function.

bool PlotIndexSetString(int index, ENUM_PLOT_PROPERTY_STRING property, string value)

The function prototype is similar to PlotIndexSetInteger except that the type of properties (value parameter) is string. The function supports only one PLOT_LABEL property (it is the ENUM_PLOT_PROPERTY_STRING enumeration constant). Custom chart index in the index parameter must be between 0 and N-1, where N is the total number of plots specified in #property indicator_plots N.

When using the directive, the chart index should be adjusted by 1 because the numbering of plots in directives starts from one, while in function parameters it starts from zero.

| Directive | Function | Description |
| --- | --- | --- |
| #property indicator_labelN | PlotIndexSetString(N-1, PLOT_LABEL, string) | Specifies a text label to display in the  Data window  and in tooltips |

For graphic series that require several indicator buffers (for example, DRAW_CANDLES, DRAW_FILLING, and others), label names are specified with the ';' separator.

Labels are also shown in a tooltip when hovering over a chart.

In the example of IndLabelHighLowClose.mq5, we add two directives (the difference from IndPropHighLowClose.mq5).

```
#property indicator_label1  "High;Low"
#property indicator_label2  "Close"

```

Now it is much easier to understand the values that appear when displaying the indicator in the Data Window.
