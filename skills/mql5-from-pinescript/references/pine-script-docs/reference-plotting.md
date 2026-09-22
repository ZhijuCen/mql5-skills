<!-- source: https://www.tradingview.com/pine-script-reference/v6/ | fetched 2026-09-23 | examples omitted -->

<!-- anchor: fun_plot -->
Plots a series of data on the chart.

#### Syntax

```
plot(series, title, color, linewidth, style, trackprice, histbase, offset, join, editable, show_last, display, format, precision, force_overlay, linestyle) → plot
```

#### Arguments

**series (series int/float) **Series of data to be plotted. Required argument.

**title (const string) **Title of the plot.

**color (series color) **Color of the plot. You can use constants like 'color=color.red' or 'color=#ff001a' as well as complex expressions like 'color = close >= open ? color.green : color.red'. Optional argument.

**linewidth (input int) **Width of the plotted line. Default value is 1. Not applicable to every style.

**style (input plot_style) **Type of plot. Possible values are: plot.style_line, plot.style_stepline, plot.style_stepline_diamond, plot.style_histogram, plot.style_cross, plot.style_area, plot.style_columns, plot.style_circles, plot.style_linebr, plot.style_areabr, plot.style_steplinebr. Default value is plot.style_line.

**trackprice (input bool) **If true then a horizontal price line will be shown at the level of the last indicator value. Default is false.

**histbase (input int/float) **The price value used as the reference level when rendering plot with plot.style_histogram, plot.style_columns or plot.style_area style. Default is 0.0.

**offset (simple int) **Shifts the plot to the left or to the right on the given number of bars. Default is 0.

**join (input bool) **If true then plot points will be joined with line, applicable only to plot.style_cross and plot.style_circles styles. Default is false.

**editable (input bool) **If true then plot style will be editable in Format dialog. Default is true.

**show_last (input int) **Optional. The number of bars, counting backwards from the most recent bar, on which the function can draw.

**display (input plot_display) **Controls where the plot's information is displayed. Display options support addition and subtraction, meaning that using `display.all - display.status_line` will display the plot's information everywhere except in the script's status line. `display.price_scale + display.status_line` will display the plot only in the price scale and status line. When `display` arguments such as `display.price_scale` have user-controlled chart settings equivalents, the relevant plot information will only appear when all settings allow for it. Possible values: display.none, display.pane, display.data_window, display.price_scale, display.status_line, display.all. Optional. The default is display.all.

**format (input string) **Determines whether the script formats the plot's values as prices, percentages, or volume values. The argument passed to this parameter supersedes the `format` parameter of the indicator(), and strategy() functions. Optional. The default is the `format` value used by the indicator()/strategy() function. Possible values: format.price, format.percent, format.volume.

**precision (input int) **The number of digits after the decimal point the plot's values show on the chart pane's y-axis, the script's status line, and the Data Window. Accepts a non-negative integer less than or equal to 16. The argument passed to this parameter supersedes the `precision` parameter of the indicator() and strategy() functions. When the function's `format` parameter uses format.volume, the `precision` parameter will not affect the result, as the decimal precision rules defined by format.volume supersede other precision settings. Optional. The default is the `precision` value used by the indicator()/strategy() function.

**force_overlay (const bool) **If true, the plotted results will display on the main chart pane, even when the script occupies a separate pane. Optional. The default is false.

**linestyle (input plot_line_style) **Optional. A modifier for plot styles that display lines. It specifies whether the plotted line is solid (plot.linestyle_solid), dashed (plot.linestyle_dashed), or dotted (plot.linestyle_dotted). The modifier applies only when the function uses one of the following `style` arguments: plot.style_line, plot.style_linebr, plot.style_stepline, plot.style_stepline_diamond, and plot.style_area. The default is plot.linestyle_solid.

#### Returns

A plot object, that can be used in fill()

#### See also

plotshape()plotchar()plotarrow()barcolor()bgcolor()fill()

<!-- anchor: fun_plotshape -->
Plots visual shapes on the chart.

#### Syntax

```
plotshape(series, title, style, location, color, offset, text, textcolor, editable, size, show_last, display, format, precision, force_overlay) → void
```

#### Arguments

**series (series int/float/bool) **Series of data to be plotted as shapes. Series is treated as a series of boolean values for all location values except location.absolute. Required argument.

**title (const string) **Title of the plot.

**style (input string) **Type of plot. Possible values are: shape.xcross, shape.cross, shape.triangleup, shape.triangledown, shape.flag, shape.circle, shape.arrowup, shape.arrowdown, shape.labelup, shape.labeldown, shape.square, shape.diamond. Default value is shape.xcross.

**location (input string) **Location of shapes on the chart. Possible values are: location.abovebar, location.belowbar, location.top, location.bottom, location.absolute. Default value is location.abovebar.

**color (series color) **Color of the shapes. You can use constants like 'color=color.red' or 'color=#ff001a' as well as complex expressions like 'color = close >= open ? color.green : color.red'. Optional argument.

**offset (simple int) **Shifts shapes to the left or to the right on the given number of bars. Default is 0.

**text (const string) **Text to display with the shape. You can use multiline text, to separate lines use '\n' escape sequence. Example: 'line one\nline two'.

**textcolor (series color) **Color of the text. You can use constants like 'textcolor=color.red' or 'textcolor=#ff001a' as well as complex expressions like 'textcolor = close >= open ? color.green : color.red'. Optional argument.

**editable (input bool) **If true then plotshape style will be editable in Format dialog. Default is true.

**size (const string) **Size of shapes on the chart. Possible values are: size.auto, size.tiny, size.small, size.normal, size.large, size.huge. Default is size.auto.

**show_last (input int) **Optional. The number of bars, counting backwards from the most recent bar, on which the function can draw.

**display (input plot_display) **Controls where the plot's information is displayed. Display options support addition and subtraction, meaning that using `display.all - display.status_line` will display the plot's information everywhere except in the script's status line. `display.price_scale + display.status_line` will display the plot only in the price scale and status line. When `display` arguments such as `display.price_scale` have user-controlled chart settings equivalents, the relevant plot information will only appear when all settings allow for it. Possible values: display.none, display.pane, display.data_window, display.price_scale, display.status_line, display.all. Optional. The default is display.all.

**format (input string) **Determines whether the script formats the plot's values as prices, percentages, or volume values. The argument passed to this parameter supersedes the `format` parameter of the indicator(), and strategy() functions. Optional. The default is the `format` value used by the indicator()/strategy() function. Possible values: format.price, format.percent, format.volume.

**precision (input int) **The number of digits after the decimal point the plot's values show on the chart pane's y-axis, the script's status line, and the Data Window. Accepts a non-negative integer less than or equal to 16. The argument passed to this parameter supersedes the `precision` parameter of the indicator() and strategy() functions. When the function's `format` parameter uses format.volume, the `precision` parameter will not affect the result, as the decimal precision rules defined by format.volume supersede other precision settings. Optional. The default is the `precision` value used by the indicator()/strategy() function.

**force_overlay (const bool) **If true, the plotted results will display on the main chart pane, even when the script occupies a separate pane. Optional. The default is false.

#### Remarks

Use plotshape() function in conjunction with 'overlay=true' indicator() parameter!

#### See also

plot()plotchar()plotarrow()barcolor()bgcolor()

<!-- anchor: fun_fill -->
Fills background between two plots or hlines with a given color.

#### Syntax & Overloads

fill(hline1, hline2, color, title, editable, fillgaps, display) → void

fill(plot1, plot2, color, title, editable, show_last, fillgaps, display) → void

fill(plot1, plot2, top_value, bottom_value, top_color, bottom_color, title, display, fillgaps, editable) → void

#### Arguments

**hline1 (hline) **The first hline object. Required argument.

**hline2 (hline) **The second hline object. Required argument.

**color (series color) **Color of the background fill. You can use constants like 'color=color.red' or 'color=#ff001a' as well as complex expressions like 'color = close >= open ? color.green : color.red'. Optional argument.

**title (const string) **Title of the created fill object. Optional argument.

**editable (input bool) **If true then fill style will be editable in Format dialog. Default is true.

**fillgaps (const bool) **Controls continuing fills on gaps, i.e., when one of the plot() calls returns an na value. When true, the last fill will continue on gaps. The default is false.

**display (input plot_simple_display) **Controls where the fill is displayed. Possible values are: display.none, display.all. Default is display.all.

Fill between two horizontal lines

Fill between two plots

Gradient fill between two horizontal lines

#### See also

plot()barcolor()bgcolor()hline()color.new()

<!-- anchor: fun_hline -->
Renders a horizontal line at a given fixed price level.

#### Syntax

```
hline(price, title, color, linestyle, linewidth, editable, display) → hline
```

#### Arguments

**price (input int/float) **Price value at which the object will be rendered. Required argument.

**title (const string) **Title of the object.

**color (input color) **Color of the rendered line. Must be a constant value (not an expression). Optional argument.

**linestyle (input hline_style) **Style of the rendered line. Possible values are: hline.style_solid, hline.style_dotted, hline.style_dashed. Optional argument.

**linewidth (input int) **Width of the rendered line. Default value is 1.

**editable (input bool) **If true then hline style will be editable in Format dialog. Default is true.

**display (input plot_simple_display) **Controls where the hline is displayed. Possible values are: display.none, display.all. Default is display.all.

#### Returns

An hline object, that can be used in fill()

#### See also

fill()

<!-- anchor: fun_barcolor -->
Set color of bars.

#### Syntax

```
barcolor(color, offset, editable, show_last, title, display) → void
```

#### Arguments

**color (series color) **Color of bars. You can use constants like 'red' or '#ff001a' as well as complex expressions like 'close >= open ? color.green : color.red'. Required argument.

**offset (simple int) **Shifts the color series to the left or to the right on the given number of bars. Default is 0.

**editable (input bool) **If true then barcolor style will be editable in Format dialog. Default is true.

**show_last (input int) **Optional. The number of bars, counting backwards from the most recent bar, on which the function can draw.

**title (const string) **Title of the barcolor. Optional argument.

**display (input plot_simple_display) **Controls where the barcolor is displayed. Possible values are: display.none, display.all. Default is display.all.

#### See also

bgcolor()plot()fill()

<!-- anchor: fun_bgcolor -->
Fill background of bars with specified color.

#### Syntax

```
bgcolor(color, offset, editable, show_last, title, display, force_overlay) → void
```

#### Arguments

**color (series color) **Color of the filled background. You can use constants like 'red' or '#ff001a' as well as complex expressions like 'close >= open ? color.green : color.red'. Required argument.

**offset (simple int) **Shifts the color series to the left or to the right on the given number of bars. Default is 0.

**editable (input bool) **If true then bgcolor style will be editable in Format dialog. Default is true.

**show_last (input int) **Optional. The number of bars, counting backwards from the most recent bar, on which the function can draw.

**title (const string) **Title of the bgcolor. Optional argument.

**display (input plot_simple_display) **Controls where the bgcolor is displayed. Possible values are: display.none, display.all. Default is display.all.

**force_overlay (const bool) **If true, the plotted results will display on the main chart pane, even when the script occupies a separate pane. Optional. The default is false.

#### See also

barcolor()plot()fill()

<!-- anchor: fun_plotcandle -->
Plots candles on the chart.

#### Syntax

```
plotcandle(open, high, low, close, title, color, wickcolor, editable, show_last, bordercolor, display, format, precision, force_overlay) → void
```

#### Arguments

**open (series int/float) **Open series of data to be used as open values of candles. Required argument.

**high (series int/float) **High series of data to be used as high values of candles. Required argument.

**low (series int/float) **Low series of data to be used as low values of candles. Required argument.

**close (series int/float) **Close series of data to be used as close values of candles. Required argument.

**title (const string) **Title of the plotcandles. Optional argument.

**color (series color) **Color of the candles. You can use constants like 'color=color.red' or 'color=#ff001a' as well as complex expressions like 'color = close >= open ? color.green : color.red'. Optional argument.

**wickcolor (series color) **The color of the wick of candles. An optional argument.

**editable (input bool) **If true then plotcandle style will be editable in Format dialog. Default is true.

**show_last (input int) **Optional. The number of bars, counting backwards from the most recent bar, on which the function can draw.

**bordercolor (series color) **The border color of candles. An optional argument.

**display (input plot_display) **Controls where the plot's information is displayed. Display options support addition and subtraction, meaning that using `display.all - display.status_line` will display the plot's information everywhere except in the script's status line. `display.price_scale + display.status_line` will display the plot only in the price scale and status line. When `display` arguments such as `display.price_scale` have user-controlled chart settings equivalents, the relevant plot information will only appear when all settings allow for it. Possible values: display.none, display.pane, display.data_window, display.price_scale, display.status_line, display.all. Optional. The default is display.all.

**format (input string) **Determines whether the script formats the plot's values as prices, percentages, or volume values. The argument passed to this parameter supersedes the `format` parameter of the indicator(), and strategy() functions. Optional. The default is the `format` value used by the indicator()/strategy() function. Possible values: format.price, format.percent, format.volume.

**precision (input int) **The number of digits after the decimal point the plot's values show on the chart pane's y-axis, the script's status line, and the Data Window. Accepts a non-negative integer less than or equal to 16. The argument passed to this parameter supersedes the `precision` parameter of the indicator() and strategy() functions. When the function's `format` parameter uses format.volume, the `precision` parameter will not affect the result, as the decimal precision rules defined by format.volume supersede other precision settings. Optional. The default is the `precision` value used by the indicator()/strategy() function.

**force_overlay (const bool) **If true, the plotted results will display on the main chart pane, even when the script occupies a separate pane. Optional. The default is false.

#### Remarks

Even if one value of open, high, low or close equal NaN then bar no draw.

The maximal value of open, high, low or close will be set as 'high', and the minimal value will be set as 'low'.

#### See also

plotbar()
