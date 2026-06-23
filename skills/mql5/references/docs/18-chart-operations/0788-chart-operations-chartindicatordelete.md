# ChartIndicatorDelete

Removes an indicator with a specified name from the specified chart window.

```
bool  ChartIndicatorDelete(
   long           chart_id,              // chart id
   int            sub_window             // number of the subwindow
   const string   indicator_shortname    // short name of the indicator
   );

```

Parameters

chart_id

[in]  Chart ID. 0 denotes the current chart.

sub_window

[in]  Number of the chart subwindow. 0 denotes the main chart subwindow.

const indicator_shortname

[in]  The short name of the indicator which is set in the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property with the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. To get the short name of an indicator use the [ChartIndicatorName()](/en/docs/chart_operations/chartindicatorname) function.

Return Value

Returns true in case of successful deletion of the indicator. Otherwise it returns false. To get [error](/en/docs/constants/errorswarnings/errorcodes) details use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

If two indicators with identical short names exist in the chart subwindow, the first one in a row will be deleted.

If other indicators on this chart are based on the values of the indicator that is being deleted, such indicators will also be deleted.

Do not confuse the indicator short name and the file name that is specified when creating an indicator using functions [iCustom()](/en/docs/indicators/icustom) and [IndicatorCreate()](/en/docs/series/indicatorcreate). If the short name of an indicator is not set explicitly, then the name of the file containing the source code of the indicator will be specified during compilation.

Deletion of an indicator from a chart doesn't mean that its calculation part will be deleted from the terminal memory. To release the indicator handle use the [IndicatorRelease()](/en/docs/series/indicatorrelease) function.

The indicator's short name should be formed correctly. It will be written to the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property using the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. It is recommended that the short name should contain values of all the input parameters of the indicator, because the indicator to be deleted from the chart by the [ChartIndicatorDelete()](/en/docs/chart_operations/chartindicatordelete) function is identified by the short name.

Example of deleting an indicator after initialization has failed:

```
//+------------------------------------------------------------------+
//|                                    Demo_ChartIndicatorDelete.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//--- plot Histogram
#property indicator_label1  "Histogram"
#property indicator_type1   DRAW_HISTOGRAM
#property indicator_color1  clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- input parameters
input int      first_param=1;
input int      second_param=2;
input int      third_param=3;
input bool     wrong_init=true;
//--- indicator buffers
double         HistogramBuffer[];
string         shortname;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
   int res=INIT_SUCCEEDED;
//--- Link the HistogramBuffer array to the indicator buffer
   SetIndexBuffer(0,HistogramBuffer,INDICATOR_DATA);
//--- Construct a short indicator name based on input parameters
   shortname=StringFormat("Demo_ChartIndicatorDelete(%d,%d,%d)",
                          first_param,second_param,third_param);
   IndicatorSetString(INDICATOR_SHORTNAME,shortname);
//--- If forced completion of an indicator is set, return a non-zero value
   if(wrong_init) res=INIT_FAILED;
   return(res);
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
//--- Starting position for working in a loop
   int start=prev_calculated-1;
   if(start<0) start=0;
//--- Fill in the indicator buffer with values
   for(int i=start;i<rates_total;i++)
     {
      HistogramBuffer[i]=close[i];
     }
//--- return value of prev_calculated for next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| A handler of the Deinit event                                    |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   PrintFormat("%s: Deinitialization reason code=%d",__FUNCTION__,reason);
   if(reason==REASON_INITFAILED)
     {
      PrintFormat("An indicator with a short name %s (file %s) deletes itself from the chart",shortname,__FILE__);
      int window=ChartWindowFind();
      bool res=ChartIndicatorDelete(0,window,shortname);
      //--- Analyse the result of call of ChartIndicatorDelete()
      if(!res)
        {
         PrintFormat("Failed to delete indicator %s from window #%d. Error code %d",
                     shortname,window,GetLastError());
        }
     }
  }

```

See also

[ChartIndicatorAdd()](/en/docs/chart_operations/chartindicatoradd), [ChartIndicatorName()](/en/docs/chart_operations/chartindicatorname), [ChartIndicatorsTotal()](/en/docs/chart_operations/chartindicatorstotal), [iCustom()](/en/docs/indicators/icustom), [IndicatorCreate()](/en/docs/series/indicatorcreate),  [IndicatorSetString()](/en/docs/customind/indicatorsetstring)
