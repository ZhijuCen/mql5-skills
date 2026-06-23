# ChartIndicatorAdd

Adds an indicator with the specified handle into a specified chart window. Indicator and chart should be generated on the same symbol and time frame.

```
bool  ChartIndicatorAdd(
   long  chart_id,                 // chart ID
   int   sub_window                // number of the sub-window
   int   indicator_handle          // handle of the indicator
   );

```

Parameters

chart_id

[in]  Chart ID. 0 means the current chart.

sub_window

[in]  The number of the chart sub-window. 0 means the main chart window. To add an indicator in a new window, the parameter must be one greater than the index of the last existing window, i.e. equal to [CHART_WINDOWS_TOTAL](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer). If the value of the parameter is greater than [CHART_WINDOWS_TOTAL](/en/docs/constants/chartconstants/enum_chart_property#enum_chart_property_integer), a new window will not be created, and the indicator will not be added.

indicator_handle

[in]  The handle of the indicator.

Return Value

The function returns true in case of success, otherwise it returns false. In order to obtain information about the [error](/en/docs/constants/errorswarnings/errorcodes), call the [GetLastError()](/en/docs/check/getlasterror) function. Error 4114 means that a chart and an added indicator differ by their symbol or time frame.

Note

If an indicator that should be drawn in a separate subwindow (for example, built-in [iMACD](/en/docs/indicators/imacd) or a custom indicator with specified [#property indicator_separate_window](/en/docs/basis/preprosessor/compilation) property) is applied to the main chart window, it may not be visible though it will still be present in the list of indicators. This means that the scale of the indicator is different from the scale of the price chart, and applied indicator's values do not fit in the displayed range of the price chart. In this case, [GetLastError()](/en/docs/check/getlasterror) returns zero code indicating the absence of an error. The values of such "invisible" indicator can be seen in Data Window and received from other MQL5 applications.

Example:

```
#property description "Expert Advisor demonstrating the work with ChartIndicatorAdd() function."
#property description "After launching on the chart (and receiving the error in Journal), open"
#property description "the Expert Advisor's properties and specify correct <symbol> and <period> parameters."
#property description "MACD indicator will be added on the chart."
 
//--- input parameters
input string          symbol="AUDUSD";    // symbol name
input ENUM_TIMEFRAMES period=PERIOD_M12;  // time frame
input int    fast_ema_period=12;          // fast MACD period
input int    slow_ema_period=26;          // slow MACD period
input int      signal_period=9;           // signal period
input ENUM_APPLIED_PRICE apr=PRICE_CLOSE; // price type for MACD calculation
 
int indicator_handle=INVALID_HANDLE;
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
  {
//---
   indicator_handle=iMACD(symbol,period,fast_ema_period,slow_ema_period,signal_period,apr);
//--- try to add the indicator on the chart
   if(!AddIndicator())
     {
      //--- AddIndicator() function refused to add the indicator on the chart
      int answer=MessageBox("Do you want to add MACD on the chart anyway?",
                            "Incorrect symbol and/or time frame for adding the indicator",
                            MB_YESNO // "Yes" and "No" selection buttons will be shown
                            );
      //--- if a user still insists on incorrect usage of ChartIndicatorAdd()
      if(answer==IDYES)
        {
         //--- first of all, a Journal entry will be made about that
         PrintFormat("Attention! %s: Trying to add MACD(%s/%s) indicator on %s/%s chart. Receiving error 4114",
                     __FUNCTION__,symbol,EnumToString(period),_Symbol,EnumToString(_Period));
         //--- receive the number of a new subwindow, to which we will try to add the indicator
         int subwindow=(int)ChartGetInteger(0,CHART_WINDOWS_TOTAL);
         //--- now make an attempt resulting in error
         if(!ChartIndicatorAdd(0,subwindow,indicator_handle))
            PrintFormat("Failed to add MACD indicator on %d chart window. Error code  %d",
                        subwindow,GetLastError());
        }
     }
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
// Expert Advisor performs nothing
  }
//+------------------------------------------------------------------+
//| Function for checking and adding the indicator on the chart      |
//+------------------------------------------------------------------+
bool AddIndicator()
  {
//--- displayed message
   string message;
//--- check if the indicator symbol and chart symbol match each other
   if(symbol!=_Symbol)
     {
      message="Displaying the use of Demo_ChartIndicatorAdd() function:";
      message=message+"\r\n";
      message=message+"Unable to add the indicator calculated on another symbol on the chart.";
      message=message+"\r\n";
      message=message+"Specify the chart symbol in Expert Advisor's property - "+_Symbol+".";
      Alert(message);
      //--- premature exit, the indicator will not be added on the chart
      return false;
     }
//--- check if the indicator's and chart's time frames match each other
   if(period!=_Period)
     {
      message="Unable to add the indicator calculated on another time frame on the chart.";
      message=message+"\r\n";
      message=message+"Specify the chart time frame in Expert Advisor properties - "+EnumToString(_Period)+".";
      Alert(message);
      //--- premature exit, the indicator will not be added on the chart
      return false;
     }
//--- all checks completed, symbol and indicator time frame match the chart
   if(indicator_handle==INVALID_HANDLE)
     {
      Print(__FUNCTION__,"  Creating MACD indicator");
      indicator_handle=iMACD(symbol,period,fast_ema_period,slow_ema_period,signal_period,apr);
      if(indicator_handle==INVALID_HANDLE)
        {
         Print("Failed to create MACD indicator. Error code ",GetLastError());
        }
     }
//--- reset the error code
   ResetLastError();
//--- apply the indicator to the chart 
   Print(__FUNCTION__,"  Adding MACD indicator on the chart");
   Print("MACD is generated on ",symbol,"/",EnumToString(period));
//--- receive the number of a new subwindow, to which MACD indicator is added
   int subwindow=(int)ChartGetInteger(0,CHART_WINDOWS_TOTAL);
   PrintFormat("Adding MACD indicator on %d chart window",subwindow);
   if(!ChartIndicatorAdd(0,subwindow,indicator_handle))
     {
      PrintFormat("Failed to add MACD indicator on %d chart window. Error code  %d",
                  subwindow,GetLastError());
     }
//--- Indicator added successfully
   return(true);
  }

```

See Also

[ChartIndicatorDelete()](/en/docs/chart_operations/chartindicatordelete), [ChartIndicatorName()](/en/docs/chart_operations/chartindicatorname), [ChartIndicatorsTotal()](/en/docs/chart_operations/chartindicatorstotal), [iCustom()](/en/docs/indicators/icustom), [IndicatorCreate()](/en/docs/series/indicatorcreate)
