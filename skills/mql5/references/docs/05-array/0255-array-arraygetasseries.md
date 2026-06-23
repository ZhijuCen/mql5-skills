# ArrayGetAsSeries

It checks direction of an array index.

```
bool  ArrayGetAsSeries(
   const void&  array[]    // array for checking
   );

```

Parameters

array

[in]  Checked array.

Return Value

Returns [true](/en/docs/basis/types/integer/boolconst), if the specified array has the AS_SERIES flag set, i.e. access to the array is performed back to front as in timeseries. A [timeseries](/en/docs/series) differs from a usual array in that the indexing of timeseries elements is performed from its end to beginning (from the newest data to old).

Note

To check whether an array belongs to timeseries, use the [ArrayIsSeries()](/en/docs/array/arrayisseries) function. Arrays of price data passed as input parameters into the [OnCalculate()](/en/docs/basis/function/events#oncalculate2) function do not obligatorily have the indexing direction the same as in timeseries. The necessary indexing direction can be set using the [ArraySetAsSeries()](/en/docs/array/arraysetasseries) function.

Example:

```
#property description "Indicator calculates absolute values of the difference between"
#property description "Open and Close or High and Low prices displaying them in a separate subwindow"
#property description "as a histrogram."
//--- indicator settings
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//---- plot
#property indicator_type1   DRAW_HISTOGRAM
#property indicator_style1  STYLE_SOLID
#property indicator_width1  3
//--- input parameters
input bool InpAsSeries=true; // Indexing direction in the indicator buffer
input bool InpPrices=true;   // Calculation prices (true - Open,Close; false - High,Low)
//--- indicator buffer
double ExtBuffer[];
//+------------------------------------------------------------------+
//| Calculating indicator values                                     |
//+------------------------------------------------------------------+
void CandleSizeOnBuffer(const int rates_total,const int prev_calculated,
                        const double &first[],const double &second[],double &buffer[])
  {
//--- start variable for calculation of bars
   int start=prev_calculated;
//--- work at the last bar if the indicator values have already been calculated at the previous tick
   if(prev_calculated>0)
      start--;
//--- define indexing direction in arrays
   bool as_series_first=ArrayGetAsSeries(first);
   bool as_series_second=ArrayGetAsSeries(second);
   bool as_series_buffer=ArrayGetAsSeries(buffer);
//--- replace indexing direction with direct one if necessary
   if(as_series_first)
      ArraySetAsSeries(first,false);
   if(as_series_second)
      ArraySetAsSeries(second,false);
   if(as_series_buffer)
      ArraySetAsSeries(buffer,false);
//--- calculate indicator values
   for(int i=start;i<rates_total;i++)
      buffer[i]=MathAbs(first[i]-second[i]);
  }
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- bind indicator buffers
   SetIndexBuffer(0,ExtBuffer);
//--- set indexing element in the indicator buffer
   ArraySetAsSeries(ExtBuffer,InpAsSeries);
//--- check for what prices the indicator is calculated
   if(InpPrices)
     {
      //--- Open and Close prices
      PlotIndexSetString(0,PLOT_LABEL,"BodySize");
      //--- set the indicator color
      PlotIndexSetInteger(0,PLOT_LINE_COLOR,clrOrange);
     }
   else
     {
      //--- High and Low prices
      PlotIndexSetString(0,PLOT_LABEL,"ShadowSize");
      //--- set the indicator color
      PlotIndexSetInteger(0,PLOT_LINE_COLOR,clrDodgerBlue);
     }
//---
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
//--- calculate the indicator according to the flag value
   if(InpPrices)
      CandleSizeOnBuffer(rates_total,prev_calculated,open,close,ExtBuffer);
   else
      CandleSizeOnBuffer(rates_total,prev_calculated,high,low,ExtBuffer);
//--- return value of prev_calculated for next call
   return(rates_total);
  }

```

See also

[Access to timeseries](/en/docs/series), [ArraySetAsSeries](/en/docs/array/arraysetasseries)
