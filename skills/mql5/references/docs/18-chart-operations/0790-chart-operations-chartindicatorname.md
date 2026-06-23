# ChartIndicatorName

Returns the short name of the indicator by the number in the indicators list on the specified chart window.

```
string  ChartIndicatorName(
   long  chart_id,      // chart id
   int   sub_window     // number of the subwindow
   int   index          // index of the indicator in the list of indicators added to the chart subwindow
   );

```

Parameters

chart_id

[in]  Chart ID. 0 denotes the current chart.

sub_window

[in]  Number of the chart subwindow. 0 denotes the main chart subwindow.

index

[in]  the index of the indicator in the list of indicators. The numeration of indicators start with zero, i.e. the first indicator in the list has the 0 index. To obtain the number of indicators in the list use the [ChartIndicatorsTotal()](/en/docs/chart_operations/chartindicatorstotal) function.

Return Value

The short name of the indicator which is set in the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property with the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. To get [error](/en/docs/constants/errorswarnings/errorcodes) details use the [GetLastError()](/en/docs/check/getlasterror) function.

Note

Do not confuse the indicator short name and the file name that is specified when creating an indicator using functions [iCustom()](/en/docs/indicators/icustom) and [IndicatorCreate()](/en/docs/series/indicatorcreate). If the short name of an indicator is not set explicitly, then the name of the file containing the source code of the indicator will be specified during compilation.

The indicator's short name should be formed correctly. It will be written to the [INDICATOR_SHORTNAME](/en/docs/constants/indicatorconstants/customindicatorproperties#enum_customind_property_string) property using the [IndicatorSetString()](/en/docs/customind/indicatorsetstring) function. It is recommended that the short name should contain values of all the input parameters of the indicator, because the indicator to be deleted from the chart by the [ChartIndicatorDelete()](/en/docs/chart_operations/chartindicatordelete) function is identified by the short name.

Example:

```
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//--- get the current chart ID and the number of its subwindows, including the main window
   long chart_id = ChartID();
   int  wnd_total= (int)ChartGetInteger(0,CHART_WINDOWS_TOTAL);
   
//--- iterate over all current chart windows in a loop
   for(int w=0; w<wnd_total; w++)
     {
      //--- get the number of indicators attached to the chart window specified by the loop index
      int ind_total=ChartIndicatorsTotal(chart_id, w);
      
      //--- print the header for the selected chart window
      PrintFormat("Chart window %d indicators: ", w);
      
      //--- get in the loop and write to the variable all the names of indicators attached to the selected window
      string ind_names="";
      for(int i=0; i<ind_total; i++)
        {
         ind_names+="  "+ChartIndicatorName(chart_id, w, i)+(i<ind_total-1 ? "\n": "");
        }
      //--- print the obtained list of names of all indicators, attached to the specified chart window, in the journal
      Print(ind_names);
     }
   /*
   result:
   Chart window 0 indicators: 
     AMA(9,2,30)
     SAR(0.02,0.20)
     Fractals
   Chart window 1 indicators: 
     RSI(14)
     AMA(9,2,30)
   Chart window 2 indicators: 
     MFI(14)
   */
  }

```

See also

[ChartIndicatorAdd()](/en/docs/chart_operations/chartindicatoradd), [ChartIndicatorDelete()](/en/docs/chart_operations/chartindicatordelete), [ChartIndicatorsTotal()](/en/docs/chart_operations/chartindicatorstotal), [iCustom()](/en/docs/indicators/icustom), [IndicatorCreate()](/en/docs/series/indicatorcreate), [IndicatorSetString()](/en/docs/customind/indicatorsetstring)
