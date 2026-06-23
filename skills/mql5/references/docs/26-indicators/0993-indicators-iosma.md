# iOsMA

The function returns the handle of the Moving Average of Oscillator indicator. The OsMA oscillator shows the difference between values of MACD and its signal line. It has only one buffer.

```
int  iOsMA(
   string              symbol,              // symbol name
   ENUM_TIMEFRAMES     period,              // period
   int                 fast_ema_period,     // period for Fast Moving Average
   int                 slow_ema_period,     // period for Slow Moving Average
   int                 signal_period,       // averaging period for their difference
   ENUM_APPLIED_PRICE  applied_price        // type of price or handle
   );

```

Parameters

symbol

[in] The symbol name of the security, the data of which should be used to calculate the indicator. The [NULL](/en/docs/basis/types/void) value means the current symbol.

period

[in] The value of the period can be one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values, 0 means the current timeframe.

fast_ema_period

[in]  Period for Fast Moving Average calculation.

slow_ema_period

[in]  Period for Slow Moving Average calculation.

signal_period

[in]  Averaging period for signal line calculation.

applied_price

[in]  The price used. Can be any of the price constants [ENUM_APPLIED_PRICE](/en/docs/constants/indicatorconstants/prices#enum_applied_price_enum) or a handle of another indicator.

Return Value

Returns the handle of a specified technical indicator,  in case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants). The computer memory can be freed from an indicator that is no more utilized, using the [IndicatorRelease()](/en/docs/series/indicatorrelease) function, to which the indicator handle is passed.

Note

In some systems this oscillator is also known as MACD histogram.

Example:

```
//+------------------------------------------------------------------+
//|                                                   Demo_iOsMA.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "The indicator demonstrates how to obtain data"
#property description "of indicator buffers for the iOsMA technical indicator."
#property description "A symbol and timeframe used for calculation of the indicator,"
#property description "are set by the symbol and period parameters."
#property description "The method of creation of the handle is set through the 'type' parameter (function type)."
#property description "All the other parameters are similar to the standard Moving Average of Oscillator."
 
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//--- the iOsMA plot
#property indicator_label1  "iOsMA"
#property indicator_type1   DRAW_HISTOGRAM
#property indicator_color1  clrSilver
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//+------------------------------------------------------------------+
//| Enumeration of the methods of handle creation                    |
//+------------------------------------------------------------------+
enum Creation
  {
   Call_iOsMA,             // use iOsMA
   Call_IndicatorCreate    // use IndicatorCreate
  };
//--- input parameters
input Creation             type=Call_iOsMA;           // type of the function 
input int                  fast_ema_period=12;        // period of fast ma
input int                  slow_ema_period=26;        // period of slow ma
input int                  signal_period=9;           // period of averaging of difference
input ENUM_APPLIED_PRICE   applied_price=PRICE_CLOSE; // type of price  
input string               symbol=" ";                // symbol 
input ENUM_TIMEFRAMES      period=PERIOD_CURRENT;     // timeframe
//--- indicator buffer
double         iOsMABuffer[];
//--- variable for storing the handle of the iAMA indicator
int    handle;
//--- variable for storing
string name=symbol;
//--- name of the indicator on a chart
string short_name;
//--- we will keep the number of values in the Moving Average indicator
int    bars_calculated=0;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- assignment of array to indicator buffer
   SetIndexBuffer(0,iOsMABuffer,INDICATOR_DATA);
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
   if(type==Call_iOsMA)
      handle=iOsMA(name,period,fast_ema_period,slow_ema_period,signal_period,applied_price);
   else
     {
      //--- fill the structure with parameters of the indicator     
      MqlParam pars[4];
      //--- period of fast ma
      pars[0].type=TYPE_INT;
      pars[0].integer_value=fast_ema_period;
      //--- period of slow ma
      pars[1].type=TYPE_INT;
      pars[1].integer_value=slow_ema_period;
      //--- period of averaging of difference between the fast and the slow moving average
      pars[2].type=TYPE_INT;
      pars[2].integer_value=signal_period;
      //--- type of price
      pars[3].type=TYPE_INT;
      pars[3].integer_value=applied_price;
      handle=IndicatorCreate(name,period,IND_OSMA,4,pars);
     }
//--- if the handle is not created
   if(handle==INVALID_HANDLE)
     {
      //--- tell about the failure and output the error code
      PrintFormat("Failed to create a handle of iOsMA for the pair %s/%s, error code is %d",
                  name,
                  EnumToString(period),
                  GetLastError());
      //--- the indicator is stopped early
      return(INIT_FAILED);
     }
//--- show the symbol/timeframe the Moving Average of Oscillator indicator is calculated for
   short_name=StringFormat("iOsMA(%s/%s,%d,%d,%d,%s)",name,EnumToString(period),
                           fast_ema_period,slow_ema_period,signal_period,EnumToString(applied_price));
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
//--- number of values copied from the iOsMA indicator
   int values_to_copy;
//--- determine the number of values calculated in the indicator
   int calculated=BarsCalculated(handle);
   if(calculated<=0)
     {
      PrintFormat("BarsCalculated() returned %d, error code %d",calculated,GetLastError());
      return(0);
     }
//--- if it is the first start of calculation of the indicator or if the number of values in the iOsMA indicator changed
//---or if it is necessary to calculated the indicator for two or more bars (it means something has changed in the price history)
   if(prev_calculated==0 || calculated!=bars_calculated || rates_total>prev_calculated+1)
     {
      //--- if the iOsMABuffer array is greater than the number of values in the iOsMA indicator for symbol/period, then we don't copy everything 
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
//--- fill the arrays with values of the iOsMA indicator
//--- if FillArrayFromBuffer returns false, it means the information is nor ready yet, quit operation
   if(!FillArrayFromBuffer(iOsMABuffer,handle,values_to_copy)) return(0);
//--- form the message
   string comm=StringFormat("%s ==>  Updated value in the indicator %s: %d",
                            TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                            short_name,
                            values_to_copy);
//--- display the service message on the chart
   Comment(comm);
//--- memorize the number of values in the Moving Average of Oscillator indicator
   bars_calculated=calculated;
//--- return the prev_calculated value for the next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Filling indicator buffers from the iOsMA indicator               |
//+------------------------------------------------------------------+
bool FillArrayFromBuffer(double &ama_buffer[],  // indicator buffer of OsMA values
                         int ind_handle,        // handle of the iOsMA indicator
                         int amount             // number of copied values
                         )
  {
//--- reset error code
   ResetLastError();
//--- fill a part of the iOsMABuffer array with values from the indicator buffer that has 0 index
   if(CopyBuffer(ind_handle,0,0,amount,ama_buffer)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iOsMA indicator, error code %d",GetLastError());
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
