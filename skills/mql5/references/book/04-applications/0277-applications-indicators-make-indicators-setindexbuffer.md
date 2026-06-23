# Assigning an array as a buffer: SetIndexBuffer

The role of indicator buffers can be performed by any [dynamic arrays](/en/book/basis/arrays/arrays_overview) of type double over the lifetime from the program start to its stop. The most common way to define such an array is at the global level. But in some cases, it is more convenient to set arrays as members of classes and then create global objects with arrays. We will consider examples of such an approach when implementing a multi-currency indicator (see example IndUnityPercent.mq5 in the section [Multicurrency and multitimeframe indicators](/en/book/applications/indicators_make/indicators_multisymbol)) and indicator of delta volume (see IndDeltaVolume.mq5 in the section [Waiting for data and managing visibility](/en/book/applications/indicators_make/indicators_wait_none)).

So, let's describe a dynamic array buffer at the global level (without sizing).

```
double buffer[];

```

It can be registered as a buffer using the special SetIndexBuffer function in the terminal. As a rule, it is called in the OnInit handler, like many other functions for setting up the indicator, which we will discuss later.

bool SetIndexBuffer(int index, double buffer[],  

   ENUM_INDEXBUFFER_TYPE mode = INDICATOR_DATA)

The function links the indicator buffer specified by index with the buffer dynamic array. The value of index must be between 0 and N - 1, where N is the number of buffers specified by the directive [#property indicator_buffers](/en/book/applications/indicators_make/indicators_buffers_plots).

Immediately after the binding, the array is not yet ready to work with data and does not even change its size, so initialization and all calculations should be performed in the OnCalculate function. You cannot change the size of a dynamic array after it has been assigned as an indicator buffer. For indicator buffers, all resizing operations are performed by the terminal itself.

The direction of indexing after linking an array with an indicator buffer is set by default as in ordinary arrays. If necessary, it can be changed using the [ArraySetAsSeries](/en/book/common/arrays/arrays_as_series) function.

The SetIndexBuffer function returns true on success and false on error.

The optional mode parameter tells the system how the buffer will be used. The possible values are provided in the ENUM_INDEXBUFFER_TYPE enum.

| Identifier | Description |
| --- | --- |
| INDICATOR_DATA | Data to render |
| INDICATOR_COLOR_INDEX | Rendering colors |
| INDICATOR_CALCULATIONS | Internal results of intermediate calculations |

By default, the indicator buffer is intended for drawing data (INDICATOR_DATA). This value has another effect besides displaying the array on the chart: the value of each buffer for the bar under the mouse cursor is shown in the Data window. However, this behavior can be changed by some indicator settings (see PLOT_SHOW_DATA property in the [Graphic plot setting](/en/book/applications/indicators_make/indicators_plotindexsetinteger) section). Most of the examples in this chapter refer to the INDICATOR_DATA mode.

If the indicator calculation requires storing intermediate results for each bar, an auxiliary non-displayed buffer (INDICATOR_CALCULATIONS) can be allocated for them. This is more convenient than using an ordinary array for the same purpose since then the programmer must independently control its size. This chapter will present two examples with INDICATOR_CALCULATIONS: IndTripleEMA.mq5 (see [Skip drawing on initial bars](/en/book/applications/indicators_make/indicators_begin)) and IndSubChartSimple.mq5 (see [Multicurrency and multitimeframe indicators](/en/book/applications/indicators_make/indicators_multisymbol)).

Some constructions allow setting the display color for each bar. Color buffers (INDICATOR_COLOR_INDEX) are used to store color information. Color is represented by integer type color, but all indicator buffers must have the type double, and in this case, they store the color number from a special palette set by the developer (see section [Element-by-element coloring of diagrams](/en/book/applications/indicators_make/indicators_color) and example indicator IndColorWPR.mq5 in it).

Color and auxiliary buffer values are not displayed in the Data window, and they cannot be obtained using the CopyBuffer function which we will explore later in the chapter on [Using built-in and custom indicators](/en/book/applications/indicators_use/indicators_copybuffer) from MQL5.

The indicator buffer is not initialized with any values. If some of its elements are not calculated for one reason or another (for example, in the indicator settings there is a limit on the maximum number of bars or the graphical construction itself implies rare significant elements between which there should be gaps, like between ZigZag vertices), then they should be explicitly filled with a special "empty" value. The empty value is not displayed on the chart and is not displayed in the Data Window. By default, there is an EMPTY_VALUE (DBL_MAX) constant for it, but if necessary, it can be replaced with any other, for example, with 0. This is done using the [PlotIndexSetDouble](/en/book/applications/indicators_make/indicators_empty_value) function.

Given the new knowledge about the function SetIndexBuffer, let's complete our next example IndReplica1.mq5, which we started in the previous section. In particular, we need the OnInit handler.

```
#property indicator_chart_window
#property indicator_buffers 1
#property indicator_plots 1
 
#include <MQL5Book/PRTF.mqh>
 
double buffer[]; // global dynamic array
 
int OnInit()
{
   // register an array as an indicator buffer
   PRTF(SetIndexBuffer(0, buffer)); // true / ok
   // the second incorrect call is made here intentionally to show an error
   PRTF(SetIndexBuffer(1, buffer)); // false / BUFFERS_WRONG_INDEX(4602)
   // check size: still 0
   PRTF(ArraySize(buffer)); // 0
   return INIT_SUCCEEDED;
}

```

The number of buffers is defined by the directive equal to 1, so the array assignment for a single buffer uses index 0 (the first parameter SetIndexBuffer). The second function call is erroneous and is only added to demonstrate the problem: since index 1 implies two declared buffers, it generates a BUFFERS_WRONG_INDEX (4602) error.

At the very beginning of the OnCalculate function, let's print the size of the array again. In this place, it will already be distributed according to the number of bars.

```
int OnCalculate(const int rates_total, 
                const int prev_calculated, 
                const int begin, 
                const double &data[])
{
   // after starting, check that the platform automatically manages the size of the array
   if(prev_calculated == 0)
   {
      PRTF(ArraySize(buffer)); // 10189 - actual number of bars
   }
   ...

```

Now let's turn to the question of what our indicator will calculate. As already mentioned, we will not put complex formulas into it yet, but simply try to copy the passed timeseries from the data parameter to the buffer. This is reflected in the name of the indicator.

```
   ...
   // on each new bar or set of bars (including the first calculation)
   if(prev_calculated != rates_total)
   {
      // fill in all new bars
      ArrayCopy(buffer, data, prev_calculated, prev_calculated);
   }
   else // ticks on the current bar
   {
      // update the last bar
      buffer[rates_total - 1] = data[rates_total - 1];
   }
   
   // we report the number of processed bars to ourselves in the future
   return rates_total;
}

```

Now the indicator is compiled without any warnings. We can run it on the chart, and with the default settings, it should duplicate the values of the closing prices of the bars in the buffer. This is due to the short form of OnCalculate, we considered this aspect in the section [Main indicator event: OnCalculate](/en/book/applications/indicators_make/indicators_oncalculate).

However, there is a strange thing: our buffer is displayed in the Data window and it contains the correct values, but there is no line on the chart. This is a consequence of the fact that graphical constructions, and not buffers, are responsible for the display. In the current version of the indicator, we have configured only the buffer. In the next section, we will create a new version IndReplica2.mq5 and supplement it with the necessary instructions.

At the same time, the described effect can be useful for creating "hidden" indicators that do not display their lines on the chart but are available for programmatic reading from other MQL programs. If desired, the developer will be able to hide even the mention of indicator buffers from Data windows (see PLOT_SHOW_DATA in the next section).

How to manage indicators from MQL5 code will be discussed in the [next chapter](/en/book/applications/indicators_use).
