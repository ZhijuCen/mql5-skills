# Indicator Styles in Examples

The MetaTrader 5 Client Terminal includes 38 technical indicators that can be used in MQL5 programs using [appropriate functions](/en/docs/indicators). But the main advantage of the MQL5 language is the ability to create custom indicators, which can then be used in Expert Advisors or simply applied on price charts for the purpose of technical analysis.

The entire set of indicators can be derived from several base [drawing styles](/en/docs/constants/indicatorconstants/drawstyles), known as plotting. Plotting denotes a way of displaying data, which the indicator calculates, stores and provides on request. There are seven such basic plotting types:

1. A line
2. A section (segment)
3. Histogram
4. Arrow (symbol)
5. A painted area (filled channel)
6. Bars
7. Japanese candlesticks

Each plotting requires one to five [arrays](/en/docs/basis/variables#array_define) of the [double](/en/docs/basis/types/double) type, in which indicator values are stored. For the purpose of convenience, these arrays are associated with the indicator buffers. The number of buffers in an indicator must be declared in advance using [compiler directives](/en/docs/basis/preprosessor/compilation), for example:

```
#property indicator_buffers 3 // Number of buffers
#property indicator_plots   2 // number of plots

```

The number of buffers in the indicator is always greater than or equal to the number of plots in the indicator.

Since each basic plotting type can have color variation or construction specifics, the actual number of plotting types in the MQL5 is 18:

| Plotting | Description | Value buffers | Color buffers |
| --- | --- | --- | --- |
| DRAW_NONE | Is not visually displayed in the chart, but the values of the corresponding buffer can be viewed in the Data Window | 1 | - |
| DRAW_LINE | A line is plotted on the values of the corresponding buffer (empty values ​​in the buffer are undesirable) | 1 | - |
| DRAW_SECTION | Is drawn as line segments between the values ​​of the corresponding buffer (usually has a lot of empty values) | 1 | - |
| DRAW_HISTOGRAM | Is drawn as a histogram from the zero line to the values ​​of the corresponding buffer (may have empty values) | 1 | - |
| DRAW_HISTOGRAM2 | Is drawn as a histogram based on two indicator buffers (may have empty values) | 2 | - |
| DRAW_ARROW | Is drawn as symbols (may have empty values) | 1 | - |
| DRAW_ZIGZAG | Similar to the style  DRAW_SECTION , but unlike it, can plot  vertical segments on one bar | 2 | - |
| DRAW_FILLING | Color fill between two lines. 2 values ​​of the corresponding buffers are shown in the Data Window | 2 | - |
| DRAW_BARS | Is drawn as bars. 4 values ​​of the corresponding buffers are shown in the Data Window | 4 | - |
| DRAW_CANDLES | Drawn as Japanese candlesticks. 4 values ​​of the corresponding buffers are shown in the Data Window | 4 | - |
| DRAW_COLOR_LINE | A line for which you can alternate colors on different bars or change its color at any time | 1 | 1 |
| DRAW_COLOR_SECTION | Similar to the style  DRAW_SECTION , but the color of each section can be set individually; color can also be set dynamically | 1 | 1 |
| DRAW_COLOR_HISTOGRAM | Similar to the style  DRAW_HISTOGRAM , but each strip may have a different color, you can set the color dynamically | 1 | 1 |
| DRAW_COLOR_HISTOGRAM2 | Similar to the style  DRAW_HISTOGRAM2 , but each strip may have a different color, you can set the color dynamically | 2 | 1 |
| DRAW_COLOR_ARROW | Similar to the style  DRAW_ARROW , but each symbol can have its color. Color can be changed dynamically | 1 | 1 |
| DRAW_COLOR_ZIGZAG | The  DRAW_ZIGZAG  style with the options of individual coloring of sections and dynamic color changing | 2 | 1 |
| DRAW_COLOR_BARS | The  DRAW_BARS  style with the options of individual coloring of bars and dynamic color changing | 4 | 1 |
| DRAW_COLOR_CANDLES | The  DRAW_CANDLES  style with the options of individual coloring of candlesticks and dynamic color changing | 4 | 1 |

### The difference between an indicator buffer and an array

In each indicator, on its [global level](/en/docs/basis/variables/global), you should declare one or more arrays of the double type, which then must be used as an indicator buffer using the [SetIndexBuffer()](/en/docs/customind/setindexbuffer) function. To draw indicator plots, only the values ​​of the indicator buffers are used, any other arrays cannot be used for this purpose. In addition, buffer values are displayed in the Data Window.

An indicator buffer should be [dynamic](/en/docs/basis/types/dynamic_array) and does not require [specification of the size](/en/docs/array/arrayresize) – the size of the array used as the indicator buffer is set by the terminal execution subsystem automatically.

After the array is bound to the indicator buffer, [the indexing direction](/en/docs/series/bufferdirection) is set by default like in ordinary arrays, but you can use the [ArraySetAsSeries()](/en/docs/array/arraysetasseries) function to change the way of access to the array elements. By default, the indicator buffer is used to store data used for plotting ([INDICATOR_DATA](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_indexbuffer_type_enum)).

If the calculation of indicator values requires holding intermediate calculations and storing the additional values for each bar, then such an array can be declared as a calculation buffer during binding ([INDICATOR_CALCULATIONS](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_indexbuffer_type_enum)). For the intermediate values, you can also use a regular array, but in this case, the programmer has to manage the size of the array.

Some plots allow setting a color for each bar. To store the information about color, color buffers are used ([INDICATOR_COLOR_INDEX](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_indexbuffer_type_enum)). The color is an integer type [color](/en/docs/basis/types/integer/color), but all indicator buffers must be of type [double](/en/docs/basis/types/double). Values of color and auxiliary (INDICATOR_CALCULATIONS) buffers cannot be obtained by using [CopyBuffer()](/en/docs/series/copybuffer).

The number of indicator buffers must be specified using the compiler directive #property indicator_buffers number_of_buffers:

```
#property indicator_buffers 3  //  the indicator has 3 buffers

```

The maximum allowed number of buffers in one indicator is 512.

### Relevance of Indicator Buffers and Plotting

Each plotting is based on one or more indicator buffers. So, for displaying simple candlesticks, four values are required - Open, High, Low and Close prices. Accordingly, to display an indicator in the form of candlesticks, it is necessary to declare 4 indicator buffers and 4 arrays of the double type for them. For example:

```
//--- The indicator has four indicator buffers
#property indicator_buffers 4
//--- The indicator has one plotting
#property indicator_plots   1
//--- Graphical plotting number 1 will appear as candlesticks
#property indicator_type1   DRAW_CANDLES
//--- Candlestick will be drawn in clrDodgerBlue
#property indicator_color1  clrDodgerBlue
//--- 4 arrays for the indicator buffers
double OBuffer[];
double HBuffer[];
double LBuffer[];
double CBuffer[];

```

Graphical plots automatically use indicator buffers in accordance with the plot number. Numbering of plots starts with 1, numbering of buffers starts with zero. If the first plotting requires 4 indicator buffers, then the first 4 indicator buffers will be used to draw it. These four buffers should be linked with the appropriate arrays with correct indexing using the [SetIndexBuffer()](/en/docs/customind/setindexbuffer) function.

```
//--- Binding arrays with indicator buffers
   SetIndexBuffer(0,OBuffer,INDICATOR_DATA);  // The first buffer corresponds to the zero index
   SetIndexBuffer(1,HBuffer,INDICATOR_DATA);  // The second buffer corresponds to index 1
   SetIndexBuffer(2,LBuffer,INDICATOR_DATA);  // The third buffer corresponds to index 2
   SetIndexBuffer(3,CBuffer,INDICATOR_DATA);  // The fourth buffer corresponds to index 3

```

The plotting candlesticks, the indicator will use just the first four buffers, because plotting of "candlesticks" was announced under the first number.

Change the example, and add plotting of a simple line - [DRAW_LINE](/en/docs/customind/indicators_examples/draw_line). Now suppose that the line is numbered 1, and the candlesticks are number 2. The number of buffers and the number of plots has increased.

```
//--- The indicator has 5 indicator buffers
#property indicator_buffers 5
//--- The indicator has 2 plots
#property indicator_plots   2
//--- Plot 1 is a line
#property indicator_type1   DRAW_LINE
//--- The color of the line is clrDodgerRed
#property indicator_color1  clrDodgerRed
//--- Plot 2 is drawn as Japanese candlesticks
#property indicator_type2   DRAW_CANDLES
//--- The color of the candlesticks is clrDodgerBlue
#property indicator_color2  clrDodgerBlue
//--- 5 arrays for indicator buffers
double LineBuffer[];
double OBuffer[];
double HBuffer[];
double LBuffer[];
double CBuffer[];

```

The order of the plots has changed, and now the line comes first, followed by Japanese candlesticks. Therefore, the order of the buffers is appropriate - first we announce a buffer for the line with the zero index, and then four buffers for the candlesticks.

```
   SetIndexBuffer(0,LineBuffer,INDICATOR_DATA);  // The first buffer corresponds to index 0
//--- Binding arrays with indicator buffers for the candlesticks
   SetIndexBuffer(1,OBuffer,INDICATOR_DATA);     // The second buffer corresponds to index 1
   SetIndexBuffer(2,HBuffer,INDICATOR_DATA);     // The third buffer corresponds to index 2
   SetIndexBuffer(3,LBuffer,INDICATOR_DATA);     // The fourth buffer corresponds to index 3
   SetIndexBuffer(4,CBuffer,INDICATOR_DATA);     // The fifth buffer corresponds to index 4 

```

The number of buffers and plots can be set only by using compiler directives, it is impossible to change these properties dynamically using functions.

### Color Versions of Styles

As can be seen in the table, the styles are divided into two groups. The first group includes styles in whose name there is no word COLOR, we call these styles basic:

- DRAW_LINE
- DRAW_SECTION
- DRAW_HISTOGRAM
- DRAW_HISTOGRAM2
- DRAW_ARROW
- DRAW_ZIGZAG
- DRAW_FILLING
- DRAW_BARS
- DRAW_CANDLES

In the second group, the style names contain the word COLOR, let's call them color versions:

- DRAW_COLOR_LINE
- DRAW_COLOR_SECTION
- DRAW_COLOR_HISTOGRAM
- DRAW_COLOR_HISTOGRAM2
- DRAW_COLOR_ARROW
- DRAW_COLOR_ZIGZAG
- DRAW_COLOR_BARS
- DRAW_COLOR_CANDLES

All color versions of styles differ from the basic ones in that they allow specifying a color for each part of the plotting. The minimal part of plotting is a bar, so we can say that the color versions allow setting the color on each bar.

Exceptions are styles [DRAW_NONE](/en/docs/customind/indicators_examples/draw_none) and [DRAW_FILLING](/en/docs/customind/indicators_examples/draw_filling), they do not have color versions.

To set the plotting color on each bar, an additional buffer for storing the color index has been added to the color version. These indices indicate the number of a color in a special array, which contains a predefined set of colors. The size of the array of colors is 64. This means that each color version of a style allows painting a plot in 64 different colors.

The set and the number of colors in the special array of colors can be set via a compiler directive #property indicator_color, where you can specify all the necessary colors separated by commas. For example, such an entry in an indicator:

```
//--- Define 8 colors for coloring candlesticks (they are stored in the special array)
#property indicator_color1  clrRed,clrBlue,clrGreen,clrYellow,clrMagenta,clrCyan,clrLime,clrOrange

```

It states that for plotting 1, 8 colors are set, which will be placed in a special array. Further in the program we will not specify the color of the plotting, but only its index. If we want to set red color for the bar number K, the color index value from an array should be set in the color buffer of the indicator. The red color is specified first in the directive, it corresponds to the index number 0.

```
  //--- set the candlestick color clrRed
  col_buffer[buffer_index]=0;

```

The set of colors is not given once and for all, it can be changed dynamically using PlotIndexSetInteger(). Example:

```
      //--- Set the color for each index as the property PLOT_LINE_COLOR
      PlotIndexSetInteger(0,                    //  The number of a graphical style
                          PLOT_LINE_COLOR,      //  Property identifier
                          plot_color_ind,       //  The index of the color, where we write the color
                          color_array[i]);      //  A new color

```

### Properties of the indicator and plotting

For indicator plots, properties can be set by means of [compiler directives](/en/docs/basis/preprosessor/compilation) and using the appropriate functions. Read more information about this in [Connection between Indicator Properties and Functions](/en/docs/customind/propertiesandfunctions). Dynamic change of indicator properties using special functions allows creating more flexible custom indicators.

### Start of Indicator Drawing on the Chart

In many cases, according to the conditions of the algorithm, it is impossible to start calculating the indicator values immediately with the current bar, since it is necessary to provide a minimum number of previous bars available in history. For example, many types of smoothing imply using an array of prices over the previous N bars, and on the basis of these values, the indicator value on the current bar is calculated.

In such cases, either there is no way to calculate the indicator values for the first N bars, or these values are not intended to be displayed on the chart and are only subsidiary for calculating further values. To avoid plotting of the indicator on the first N bars of the history, set the N value to the [PLOT_DRAW_BEGIN](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_integer) property for the corresponding plot:

```
//--- Binding arrays with indicator buffers for the candlesticks
PlotIndexSetInteger(number_of_plot,PLOT_DRAW_BEGIN,N);

```

Here:

- number_of_plot – a value from zero to indicator_plots-1 (numbering of plots starts with zero).
- N - the number of first bars in the history, on which the indicator should not be displayed on the chart.
