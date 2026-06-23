# iWPR

The function returns the handle of the Larry Williams' Percent Range indicator. It has only one buffer.

```
int  iWPR(
   string           symbol,          // symbol name
   ENUM_TIMEFRAMES  period,          // period
   int              calc_period      // averaging period
   );

```

Parameters

symbol

[in] The symbol name of the security, the data of which should be used to calculate the indicator. The [NULL](/en/docs/basis/types/void) value means the current symbol.

period

[in] The value of the period can be one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values, 0 means the current timeframe.

calc_period

[in]  Period (bars count) for the indicator calculation.

Return Value

Returns the handle of a specified technical indicator,  in case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants). The computer memory can be freed from an indicator that is no more utilized, using the [IndicatorRelease()](/en/docs/series/indicatorrelease) function, to which the indicator handle is passed.

Example:

```
//+------------------------------------------------------------------+
//|                                                    Demo_iWPR.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "The indicator demonstrates how to obtain data"
#property description "of indicator buffers for the iWPR technical indicator."
#property description "A symbol and timeframe used for calculation of the indicator,"
#property description "are set by the symbol and period parameters."
#property description "The method of creation of the handle is set through the 'type' parameter (function type)."
 
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//--- the iWPR plot
#property indicator_label1  "iWPR"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrCyan
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//--- set limit of the indicator values
#property indicator_minimum -100
#property indicator_maximum 0
//--- horizontal levels in the indicator window
#property indicator_level1  -20.0
#property indicator_level2  -80.0
//+------------------------------------------------------------------+
//| Enumeration of the methods of handle creation                    |
//+------------------------------------------------------------------+
enum Creation
  {
   Call_iWPR,              // use iWPR
   Call_IndicatorCreate    // use IndicatorCreate
  };
//--- input parameters
input Creation             type=Call_iWPR;            // type of the function
input int                  calc_period=14;            // period
input string               symbol=" ";                // symbol 
input ENUM_TIMEFRAMES      period=PERIOD_CURRENT;     // timeframe
//--- indicator buffer
double         iWPRBuffer[];
//--- variable for storing the handle of the iWPR indicator
int    handle;
//--- variable for storing
string name=symbol;
//--- name of the indicator on a chart
string short_name;
//--- we will keep the number of values in the Larry Williams' Percent Range indicator
int    bars_calculated=0;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- assignment of array to indicator buffer
   SetIndexBuffer(0,iWPRBuffer,INDICATOR_DATA);
//--- determine the symbol the indicator is drawn for
   name=symbol;
//--- delete spaces to the right and to the left
   StringTrimRight(name);
   StringTrimLeft(name);
//--- if it results in zero length of the 'name' string
   if(StringLen(name)==0)
     {
      //--- take the symbol of the chart the indicator is attached to
      name=_Symbol;
     }
//--- create handle of the indicator
   if(type==Call_iWPR)
      handle=iWPR(name,period,calc_period);
   else
     {
      //--- fill the structure with parameters of the indicator     
      MqlParam pars[1];
      //--- period
      pars[0].type=TYPE_INT;
      pars[0].integer_value=calc_period;
      handle=IndicatorCreate(name,period,IND_WPR,1,pars);
     }
//--- if the handle is not created
   if(handle==INVALID_HANDLE)
     {
      //--- tell about the failure and output the error code
      PrintFormat("Failed to create handle of the iWPR indicator for the symbol %s/%s, error code %d",
                  name,
                  EnumToString(period),
                  GetLastError());
      //--- the indicator is stopped early
      return(INIT_FAILED);
     }
//--- show the symbol/timeframe the Williams' Percent Range indicator is calculated for
   short_name=StringFormat("iWPR(%s/%s, %d)",name,EnumToString(period),calc_period);
   IndicatorSetString(INDICATOR_SHORTNAME,short_name);
//--- normal initialization of the indicator
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
//--- number of values copied from the iWPR indicator
   int values_to_copy;
//--- determine the number of values calculated in the indicator
   int calculated=BarsCalculated(handle);
   if(calculated<=0)
     {
      PrintFormat("BarsCalculated() returned %d, error code %d",calculated,GetLastError());
      return(0);
     }
//--- if it is the first start of calculation of the indicator or if the number of values in the iWPR indicator changed
//---or if it is necessary to calculated the indicator for two or more bars (it means something has changed in the price history)
   if(prev_calculated==0 || calculated!=bars_calculated || rates_total>prev_calculated+1)
     {
      //--- if the iWPRBuffer array is greater than the number of values in the iWPR indicator for symbol/period, then we don't copy everything 
      //--- otherwise, we copy less than the size of indicator buffers
      if(calculated>rates_total) values_to_copy=rates_total;
      else                       values_to_copy=calculated;
     }
   else
     {
      //--- it means that it's not the first time of the indicator calculation, and since the last call of OnCalculate()
      //--- for calculation not more than one bar is added
      values_to_copy=(rates_total-prev_calculated)+1;
     }
//--- fill the array with values of the Williams' Percent Range indicator
//--- if FillArrayFromBuffer returns false, it means the information is nor ready yet, quit operation
   if(!FillArrayFromBuffer(iWPRBuffer,handle,values_to_copy)) return(0);
//--- form the message
   string comm=StringFormat("%s ==>  Updated value in the indicator %s: %d",
                            TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                            short_name,
                            values_to_copy);
//--- display the service message on the chart
   Comment(comm);
//--- memorize the number of values in the Larry Williams' Percent Range indicator
   bars_calculated=calculated;
//--- return the prev_calculated value for the next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Filling indicator buffers from the iWPR indicator                |
//+------------------------------------------------------------------+
bool FillArrayFromBuffer(double &wpr_buffer[],  // indicator buffer of Williams' Percent Range values
                         int ind_handle,        // handle of the iWPR indicator
                         int amount             // number of copied values
                         )
  {
//--- reset error code
   ResetLastError();
//--- fill a part of the iWPRBuffer array with values from the indicator buffer that has 0 index
   if(CopyBuffer(ind_handle,0,0,amount,wpr_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iWPR indicator, error code %d",GetLastError());
      //--- quit with zero result - it means that the indicator is considered as not calculated
      return(false);
     }
//--- everything is fine
   return(true);
  }
//+------------------------------------------------------------------+
//| Indicator deinitialization function                              |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   if(handle!=INVALID_HANDLE)
      IndicatorRelease(handle);
//--- clear the chart after deleting the indicator
   Comment("");
  }

```
