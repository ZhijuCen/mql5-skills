# Setting the number of buffers and graphic plots

For the indicator to display the results of its calculations on the chart, it must define one or more arrays and declare them as indicator buffers. The number of buffers is set using the directive:

```
#property indicator_buffers N

```

Here N is an integer from 1 to 512. This directive sets the number of buffers that will be available in the code for calculating the indicator.

N must be an integer constant (literal) or equivalent macro definition. Since this is a preprocessor directive, no variables (even with the const modifier) exist yet at the source code preprocessing stage.

However, buffers are not enough to visualize the calculated data. In MQL5, the visualization system is two-level. The first level is formed by indicator buffers, which are dynamic arrays that store data for display. The second level is for managing how this data will be displayed. It is built on the basis of new entities called graphical constructions (or diagrams, or plots). The point is that different ways of displaying data may require different numbers of indicator buffers. For example, the moving average has exactly one value per bar, and therefore one indicator buffer is sufficient for such a line chart. However, to display a candlestick chart, 4 values per bar (OHLC prices) are required. Thus, one such graphic plot requires 4 indicator buffers.

The number of charts (P) must also be defined in the source code using a special directive.

```
#property indicator_plots   P

```

In the simplest case, the number of buffers and diagrams is the same. But we will soon analyze examples when you need more buffers than graphical constructions. In addition to situations in which the graphical construction of a particular type requires a predetermined number of buffers, we sometimes have to deal with the need to allocate one or more arrays for intermediate calculations. Such arrays are not directly involved in rendering but contain data for building rendered buffers. Of course, you can use simple dynamic arrays for such purposes without declaring them as buffers. But then we would have to independently control and resize them. It is much more convenient to make them buffers and thus instruct the terminal to allocate memory.

The number of buffers and graphical plots can only be set using preprocessor directives; these properties cannot be changed dynamically using MQL5 functions.

After the number of buffers and charts is determined, the arrays themselves, which will become indicator buffers, should be described in the source code.

Let's start developing a new indicator example IndReplica1.mq5 to demonstrate the necessary parts in the source code. The essence of the indicator will be simple: in its only buffer, we will display the values of the received data parameter array. As we said earlier, a specific timeseries to transfer to the data array is selected by the user at the moment the indicator is applied to the chart; a timeseries with bar close prices will be offered by default.

Let's add directives describing one buffer and one chart.

```
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots 1

```

The directives do not allocate the buffer itself, but only set the properties of the indicator and prepare the runtime system for the program to further determine and configure the specified number of arrays. Next, let's see how to register an array as a buffer.
