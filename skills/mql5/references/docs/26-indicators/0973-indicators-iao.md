# iAO

The function returns the handle of the Awesome Oscillator indicator. It has only one buffer.

```
int  iAO(
   string           symbol,     // symbol name
   ENUM_TIMEFRAMES  period      // period
   );

```

Parameters

symbol

[in] The symbol name of the security, the data of which should be used to calculate the indicator. The [NULL](/en/docs/basis/types/void) value means the current symbol.

period

[in] The value of the period can be one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values, 0 means the current timeframe.

Return Value

Returns the handle of a specified technical indicator,  in case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants). The computer memory can be freed from an indicator that is no more utilized, using the [IndicatorRelease()](/en/docs/series/indicatorrelease) function, to which the indicator handle is passed.

Example:

```
//+------------------------------------------------------------------+
//|                                                     Demo_iAO.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                              https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "The indicator demonstrates how to obtain data"
#property description "of indicator buffers for the iAO technical indicator."
#property description "A symbol and timeframe used for calculation of the indicator,"
#property description "are set by the symbol and period parameters."
#property description "The method of creation of the handle is set through the 'type' parameter (function type)."
 
#property indicator_separate_window
#property indicator_buffers 2
#property indicator_plots   1
//--- the iAO plot
#property indicator_label1  "iAO"
#property indicator_type1   DRAW_COLOR_HISTOGRAM
#property indicator_color1  clrGreen,clrRed
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//+------------------------------------------------------------------+
//| Enumeration of the methods of handle creation                    |
//+------------------------------------------------------------------+
enum Creation
  {
   Call_iAO,               // use iAO
   Call_IndicatorCreate    // use IndicatorCreate
  };
//--- input parameters
input Creation             type=Call_iAO;          // type of the function 
input string               symbol=" ";             // symbol
input ENUM_TIMEFRAMES      period=PERIOD_CURRENT;  // timeframe
//--- indicator buffers
double         iAOBuffer[];
double         iAOColors[];
//--- variable for storing the handle of the iAO indicator
int    handle;
//--- variable for storing
string name=symbol;
//--- name of the indicator on a chart
string short_name;
//--- we will keep the number of values in the Awesome Oscillator indicator
int    bars_calculated=0;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- assignment of arrays to indicator buffers
   SetIndexBuffer(0,iAOBuffer,INDICATOR_DATA);
   SetIndexBuffer(1,iAOColors,INDICATOR_COLOR_INDEX);
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
   if(type==Call_iAO)
      handle=iAO(name,period);
   else
      handle=IndicatorCreate(name,period,IND_AO);
//--- if the handle is not created
   if(handle==INVALID_HANDLE)
     {
      //--- tell about the failure and output the error code
      PrintFormat("Failed to create handle of the iAO indicator for the symbol %s/%s, error code %d",
                  name,
                  EnumToString(period),
                  GetLastError());
      //--- the indicator is stopped early
      return(INIT_FAILED);
     }
//--- show the symbol/timeframe the Awesome Oscillator indicator is calculated for
   short_name=StringFormat("iAO(%s/%s)",name,EnumToString(period));
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
//--- number of values copied from the iAO indicator
   int values_to_copy;
//--- determine the number of values calculated in the indicator
   int calculated=BarsCalculated(handle);
   if(calculated<=0)
     {
      PrintFormat("BarsCalculated() returned %d, error code %d",calculated,GetLastError());
      return(0);
     }
//--- if it is the first start of calculation of the indicator or if the number of values in the iAO indicator changed
//---or if it is necessary to calculated the indicator for two or more bars (it means something has changed in the price history)
   if(prev_calculated==0 || calculated!=bars_calculated || rates_total>prev_calculated+1)
     {
      //--- if the iAOBuffer array is greater than the number of values in the iAO indicator for symbol/period, then we don't copy everything 
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
//--- fill the iAOBuffer and iAOColors arrays with values from the Awesome Oscillator indicator
//--- if FillArraysFromBuffer returns false, it means the information is nor ready yet, quit operation
   if(!FillArraysFromBuffer(iAOBuffer,iAOColors,handle,values_to_copy)) return(0);
//--- form the message
   string comm=StringFormat("%s ==>  Updated value in the indicator %s: %d",
                            TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                            short_name,
                            values_to_copy);
//--- display the service message on the chart
   Comment(comm);
//--- memorize the number of values in the Awesome Oscillator indicator
   bars_calculated=calculated;
//--- return the prev_calculated value for the next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Filling indicator buffers from the iAO indicator                 |
//+------------------------------------------------------------------+
bool FillArraysFromBuffer(double &values[],        // indicator buffer of Awesome Oscillator values
                          double &color_indexes[], // color buffer (for storing of color indexes)
                          int ind_handle,          // handle of the iAO indicator
                          int amount               // number of copied values
                          )
  {
//--- reset error code
   ResetLastError();
//--- fill a part of the iAOBuffer array with values from the indicator buffer that has 0 index
   if(CopyBuffer(ind_handle,0,0,amount,values)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iAO indicator, error code %d",GetLastError());
      //--- quit with zero result - it means that the indicator is considered as not calculated
      return(false);
     }
//--- now copy the indexes of colors
   if(CopyBuffer(ind_handle,1,0,amount,color_indexes)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy color values from the iAO indicator, error code %d",GetLastError());
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
