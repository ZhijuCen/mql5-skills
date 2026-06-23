# CopyTickVolume

The function gets into volume_array the history data of tick volumes for the selected symbol-period pair in the specified quantity. It should be noted that elements ordering is from present to past, i.e., starting position of 0 means the current bar.

![When copying the yet unknown amount of data, it  is recommended to use  dynamic array  as a target array, because if the requested data count is less (or more) than the length of the target array, function  tries to reallocate the memory so that the requested data fit entirely.](pics/copytickvolume.png)

When copying the yet unknown amount of data, it is recommended to use [dynamic array](/en/docs/basis/types/dynamic_array) as a target array, because if the requested data count is less (or more) than the length of the target array, function tries to reallocate the memory so that the requested data fit entirely.

If you know the amount of data you need to copy, it should better be done to a [statically allocated buffer](/en/docs/basis/types/dynamic_array#static_array), in order to prevent the allocation of excessive memory.

No matter what is the property of the target array - as_series=true or as_series=false. Data will be copied so that the oldest element will be located at the start of the physical memory allocated for the array. There are 3 variants of function calls.

Call by the first position and the number of required elements

```
int  CopyTickVolume(
   string           symbol_name,      // symbol name
   ENUM_TIMEFRAMES  timeframe,        // period
   int              start_pos,        // start position
   int              count,            // data count to copy
   long             volume_array[]    // target array for tick volumes
   );

```

Call by the start date and the number of required elements

```
int  CopyTickVolume(
   string           symbol_name,      // symbol name
   ENUM_TIMEFRAMES  timeframe,        // period
   datetime         start_time,       // start date and time
   int              count,            // data count to copy
   long             volume_array[]    // target array for tick volumes
   );

```

Call by the start and end dates of a required time interval

```
int  CopyTickVolume(
   string           symbol_name,      // symbol name
   ENUM_TIMEFRAMES  timeframe,        // period
   datetime         start_time,       // start date and time
   datetime         stop_time,        // stop date and time
   long             volume_array[]    // target array for tick volumes
   );

```

Parameters

symbol_name

[in]  Symbol name.

timeframe

[in]  Period.

start_pos

[in]  The start position for the first element to copy.

count

[in]  Data count to copy.

start_time

[in]  The start time for the first element to copy.

stop_time

[in]  Bar time, corresponding to the last element to copy.

volume_array[]

[out]  Array of  [long](/en/docs/basis/types/integer/integertypes) type.

Return Value

Returns the copied data count or -1 in case of an [error](/en/docs/constants/errorswarnings/errorcodes).

Note

If the whole interval of requested data is out of the available data on the server, the function returns -1. If data outside [TERMINAL_MAXBARS](/en/docs/constants/environment_state/terminalstatus) (maximal number of bars on the chart) is requested, the function will also return -1.

When requesting data from the indicator, if requested timeseries are not yet built or they need to be downloaded from the server, the function will immediately return -1, but the process of downloading/building will be initiated.

When requesting data from an Expert Advisor or script, [downloading from the server](/en/docs/series/timeseries_access#synchronized) will be initiated, if  the terminal does not have these data locally, or building of a required timeseries will start, if data can be built from the local history but they are not ready yet. The function will return the amount of data that will be ready by the moment of timeout expiration, but history downloading will continue, and at the next similar request the function will return more data.

When requesting data by the start date and the number of required elements, only data whose date is less than (earlier) or equal to the date specified will be returned. It means, the open time of any bar, for which value is returned (volume, spread, value on the indicator buffer, prices Open, High, Low, Close or open time Time) is always less or equal to the specified one.

When requesting data in a specified range of dates, only data from this interval will be returned. The interval is set and counted up to seconds. It means, the open time of any bar, for which value is returned (volume, spread, value on the indicator buffer, prices Open, High, Low, Close or open time Time) is always within the requested interval.

Thus, if the current day is Saturday, at the attempt to copy data on a week timeframe specifying start_time=Last_Tuesday and stop_time=Last_Friday the function will return 0, because the open time on a week timeframe is always Sunday, but one week bar does not fall into the specified interval.

If you need to return value corresponding to the current uncompleted bar, you can use the first form of call specifying start_pos=0 and count=1.

Example:

```
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//---- plot TickVolume
#property indicator_label1  "TickVolume"
#property indicator_type1   DRAW_HISTOGRAM
#property indicator_color1  C'143,188,139'
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- input parameters
input int      bars=3000;
//--- indicator buffers
double         TickVolumeBuffer[];
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
void OnInit()
  {
//--- indicator buffers mapping
   SetIndexBuffer(0,TickVolumeBuffer,INDICATOR_DATA);
   IndicatorSetInteger(INDICATOR_DIGITS,0);
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
   if(prev_calculated==0)
     {
      long timeseries[];
      ArraySetAsSeries(timeseries,true);
      int prices=CopyTickVolume(Symbol(),0,0,bars,timeseries);
      for(int i=0;i<rates_total-prices;i++) TickVolumeBuffer[i]=0.0; 
      for(int i=0;i<prices;i++) TickVolumeBuffer[rates_total-1-i]=timeseries[prices-1-i]; 
      Print("We have received the following number of TickVolume values: "+prices);
     }
   else
     {
      long timeseries[];
      int prices=CopyTickVolume(Symbol(),0,0,1,timeseries);
      TickVolumeBuffer[rates_total-1]=timeseries[0]; 
     }  
//--- return value of prev_calculated for next call
   return(rates_total);
  }

```

See a detailed example of history data requesting in section [Methods of Object Binding](/en/docs/constants/objectconstants/enum_anchorpoint). The script available in that section shows how to get the values of indicator [iFractals](/en/docs/indicators/ifractals) on the last 1000 bars and how to display the last 10 up and 10 down fractals on the chart. A similar technique can be used for all indicators that have missing data and that are usually drawn using the following [styles](/en/docs/customind/indicators_examples):

- [DRAW_SECTION](/en/docs/customind/indicators_examples/draw_section),
- [DRAW_ARROW](/en/docs/customind/indicators_examples/draw_arrow),
- [DRAW_ZIGZAG](/en/docs/customind/indicators_examples/draw_zigzag),
- [DRAW_COLOR_SECTION](/en/docs/customind/indicators_examples/draw_color_section),
- [DRAW_COLOR_ARROW](/en/docs/customind/indicators_examples/draw_color_arrow),
- [DRAW_COLOR_ZIGZAG](/en/docs/customind/indicators_examples/draw_color_zigzag).
