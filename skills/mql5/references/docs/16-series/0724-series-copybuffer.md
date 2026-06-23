# CopyBuffer

Gets data of a specified buffer of a certain indicator in the necessary quantity.

![Counting of elements of copied data (indicator buffer with the index buffer_num) from the starting position is performed from the present to the past, i.e., starting position of 0 means the current bar (indicator value for the current bar).](pics/copybuffer.png)

Counting of elements of copied data (indicator buffer with the index buffer_num) from the starting position is performed from the present to the past, i.e., starting position of 0 means the current bar (indicator value for the current bar).

When copying the yet unknown amount of data, it is recommended to use a [dynamic array](/en/docs/basis/types/dynamic_array) as a buffer[] recipient buffer, because the CopyBuffer() function tries to allocate the size of the receiving array to the size of the copied data. If an indicator buffer (array that is pre-allocated for storing indicator values by the [SetIndexBufer()](/en/docs/customind/setindexbuffer) function) is used as the buffer[] recipient array, partial copying is allowed. An example can be found in the Awesome_Oscillator.mql5 custom indicator in the standard terminal package.

If you need to make a partial copy of the indicator values into another array (non-indicator buffer), you should use an intermediate array, to which the desired number is copied. After that conduct the element-wise copying of the required number of values into the required places of a receiving array from this intermediate one.

If you know the amount of data you need to copy, it should better be done to a [statically allocated buffer](/en/docs/basis/types/dynamic_array#static_array), in order to prevent the allocation of excessive memory.

No matter what is the property of the target array - as_series=true or as_series=false. Data will be copied so that the oldest element will be located at the start of the physical memory allocated for the array. There are 3 variants of function calls.

Call by the first position and the number of required elements

```
int  CopyBuffer(
   int       indicator_handle,     // indicator handle
   int       buffer_num,           // indicator buffer number
   int       start_pos,            // start position
   int       count,                // amount to copy
   double    buffer[]              // target array to copy
   );

```

Call by the start date and the number of required elements

```
int  CopyBuffer(
   int       indicator_handle,     // indicator handle
   int       buffer_num,           // indicator buffer number
   datetime  start_time,           // start date and time
   int       count,                // amount to copy
   double    buffer[]              // target array to copy
   );

```

Call by the start and end dates of a required time interval

```
int  CopyBuffer(
   int       indicator_handle,     // indicator handle
   int       buffer_num,           // indicator buffer number
   datetime  start_time,           // start date and time
   datetime  stop_time,            // end date and time
   double    buffer[]              // target array to copy
   );

```

Parameters

indicator_handle

[in]  The indicator handle, returned by the corresponding indicator function.

buffer_num

[in]  The indicator buffer number.

start_pos

[in]  The position of the first element to copy.

count

[in]  Data count to copy.

start_time

[in]  Bar time, corresponding to the first element.

stop_time

[in]  Bar time, corresponding to the last element.

buffer[]

[out]  Array of [double](/en/docs/basis/types/double) type.

Return Value

Returns the copied data count or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

When requesting data from the indicator, if requested timeseries are not yet built or they need to be downloaded from the server, the function will immediately return -1, but the process of downloading/building will be initiated.

When requesting data from an Expert Advisor or script, [downloading from the server](/en/docs/series/timeseries_access#synchronized) will be initiated, if  the terminal does not have these data locally, or building of a required timeseries will start, if data can be built from the local history but they are not ready yet. The function will return the amount of data that will be ready by the moment of timeout expiration.

Example:

```
//+------------------------------------------------------------------+
//|                                              TestCopyBuffer3.mq5 |
//|                        Copyright 2009, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "2009, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
 
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//---- plot MA
#property indicator_label1  "MA"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- input parameters
input bool               AsSeries=true;
input int                period=15;
input ENUM_MA_METHOD     smootMode=MODE_EMA;
input ENUM_APPLIED_PRICE price=PRICE_CLOSE;
input int                shift=0;
//--- indicator buffers
double                   MABuffer[];
int                      ma_handle;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,MABuffer,INDICATOR_DATA);
   Print("Parameter AsSeries = ",AsSeries);
   Print("Indicator buffer after SetIndexBuffer() is a timeseries = ",
         ArrayGetAsSeries(MABuffer));
//--- set short indicator name
   IndicatorSetString(INDICATOR_SHORTNAME,"MA("+period+")"+AsSeries);
//--- set AsSeries (depends on input parameter)
   ArraySetAsSeries(MABuffer,AsSeries);
   Print("Indicator buffer after ArraySetAsSeries(MABuffer,true); is a timeseries = ",
         ArrayGetAsSeries(MABuffer));
//---
   ma_handle=iMA(Symbol(),0,period,shift,smootMode,price);
   return(INIT_SUCCEEDED);
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
//--- check if all data calculated
   if(BarsCalculated(ma_handle)<rates_total) return(0);
//--- we can copy not all data
   int to_copy;
   if(prev_calculated>rates_total || prev_calculated<=0) to_copy=rates_total;
   else
     {
      to_copy=rates_total-prev_calculated;
      //--- last value is always copied
      to_copy++;
     }
//--- try to copy
   if(CopyBuffer(ma_handle,0,0,to_copy,MABuffer)<=0) return(0);
//--- return value of prev_calculated for next call
   return(rates_total);
  }
//+------------------------------------------------------------------+

```

The above example illustrates how an indicator buffer is filled out with the values of another indicator buffer from the indicator on the same symbol/period.

See a detailed example of history requesting data in section [Methods of Object Binding](/en/docs/constants/objectconstants/enum_anchorpoint). The script available in that section shows how to get the values of indicator [iFractals](/en/docs/indicators/ifractals) on the last 1000 bars and how to display the last 10 up and 10 down fractals on the chart. A similar technique can be used for all indicators that have missing data and that are usually drawn using the following [styles](/en/docs/customind/indicators_examples):

- [DRAW_SECTION](/en/docs/customind/indicators_examples/draw_section),
- [DRAW_ARROW](/en/docs/customind/indicators_examples/draw_arrow),
- [DRAW_ZIGZAG](/en/docs/customind/indicators_examples/draw_zigzag),
- [DRAW_COLOR_SECTION](/en/docs/customind/indicators_examples/draw_color_section),
- [DRAW_COLOR_ARROW](/en/docs/customind/indicators_examples/draw_color_arrow),
- [DRAW_COLOR_ZIGZAG](/en/docs/customind/indicators_examples/draw_color_zigzag).

See also

[Properties of Custom Indicators](/en/docs/constants/indicatorconstants/customindicatorproperties), [SetIndexBuffer](/en/docs/customind/setindexbuffer)
