# iChaikin

The function returns the handle of the Chaikin Oscillator indicator. It has only one buffer.

```
int  iChaikin(
   string               symbol,             // symbol name
   ENUM_TIMEFRAMES      period,             // period
   int                  fast_ma_period,     // fast period
   int                  slow_ma_period,     // slow period
   ENUM_MA_METHOD       ma_method,          // smoothing type
   ENUM_APPLIED_VOLUME  applied_volume      // type of volume
   );

```

Parameters

symbol

[in] The symbol name of the security, the data of which should be used to calculate the indicator. The [NULL](/en/docs/basis/types/void) value means the current symbol.

period

[in] The value of the period can be one of the [ENUM_TIMEFRAMES](/en/docs/constants/chartconstants/enum_timeframes) values, 0 means the current timeframe.

fast_ma_period

[in] Fast averaging period for calculations.

slow_ma_period

[in] Slow averaging period for calculations.

ma_method

[in]  Smoothing type. Can be one of the averaging constants of [ENUM_MA_METHOD](/en/docs/constants/indicatorconstants/enum_ma_method).

applied_volume

[in]  The volume used. Can be one of the constants of [ENUM_APPLIED_VOLUME](/en/docs/constants/indicatorconstants/prices#enum_applied_volume_enum).

Return Value

Returns the handle of a specified technical indicator,  in case of failure returns [INVALID_HANDLE](/en/docs/constants/namedconstants/otherconstants). The computer memory can be freed from an indicator that is no more utilized, using the [IndicatorRelease()](/en/docs/series/indicatorrelease) function, to which the indicator handle is passed.

Example:

```
//+------------------------------------------------------------------+
//|                                                Demo_iChaikin.mq5 |
//|                        Copyright 2011, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2000-2024, MetaQuotes Ltd."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property description "The indicator demonstrates how to obtain data"
#property description "of indicator buffers for the iChaikin technical indicator."
#property description "A symbol and timeframe used for calculation of the indicator,"
#property description "are set by the symbol and period parameters."
#property description "The method of creation of the handle is set through the 'type' parameter (function type)."
 
#property indicator_separate_window
#property indicator_buffers 1
#property indicator_plots   1
//--- the iChaikin plot
#property indicator_label1  "iChaikin"
#property indicator_type1   DRAW_LINE
#property indicator_color1  clrLightSeaGreen
#property indicator_style1  STYLE_SOLID
#property indicator_width1  1
//+------------------------------------------------------------------+
//| Enumeration of the methods of handle creation                    |
//+------------------------------------------------------------------+
enum Creation
  {
   Call_iChaikin,          // use iChaikin
   Call_IndicatorCreate    // use IndicatorCreate
  };
//--- input parameters
input Creation             type=Call_iChaikin;           // type of the function 
input int                  fast_ma_period=3;             // period of fast ma
input int                  slow_ma_period=10;            // period of slow ma
input ENUM_MA_METHOD       ma_method=MODE_EMA;           // type of smoothing
input ENUM_APPLIED_VOLUME  applied_volume=VOLUME_TICK;   // type of volume
input string               symbol=" ";                   // symbol 
input ENUM_TIMEFRAMES      period=PERIOD_CURRENT;        // timeframe
//--- indicator buffer
double         iChaikinBuffer[];
//--- variable for storing the handle of the iChaikin indicator
int    handle;
//--- variable for storing
string name=symbol;
//--- name of the indicator on a chart
string short_name;
//--- we will keep the number of values in the Chaikin Oscillator indicator
int    bars_calculated=0;
//+------------------------------------------------------------------+
//| Custom indicator initialization function                         |
//+------------------------------------------------------------------+
int OnInit()
  {
//--- assignment of array to indicator buffer
   SetIndexBuffer(0,iChaikinBuffer,INDICATOR_DATA);
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
   if(type==Call_iChaikin)
      handle=iChaikin(name,period,fast_ma_period,slow_ma_period,ma_method,applied_volume);
   else
     {
      //--- fill the structure with parameters of the indicator
      MqlParam pars[4];
      //--- period of fast ma 
      pars[0].type=TYPE_INT;
      pars[0].integer_value=fast_ma_period;
      //--- period of slow ma
      pars[1].type=TYPE_INT;
      pars[1].integer_value=slow_ma_period;
      //--- type of smoothing
      pars[2].type=TYPE_INT;
      pars[2].integer_value=ma_method;
      //--- type of volume
      pars[3].type=TYPE_INT;
      pars[3].integer_value=applied_volume;
      handle=IndicatorCreate(name,period,IND_CHAIKIN,4,pars);
     }
//--- if the handle is not created
   if(handle==INVALID_HANDLE)
     {
      //--- tell about the failure and output the error code
      PrintFormat("Failed to create handle of the iChaikin indicator for the symbol %s/%s, error code %d",
                  name,
                  EnumToString(period),
                  GetLastError());
      //--- the indicator is stopped early
      return(INIT_FAILED);
     }
//--- show the symbol/timeframe the Chaikin Oscillator indicator is calculated for
   short_name=StringFormat("iChaikin(%s/%s, %d, %d, %s, %s)",name,EnumToString(period),
                           fast_ma_period,slow_ma_period,
                           EnumToString(ma_method),EnumToString(applied_volume));
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
//--- number of values copied from the iChaikin indicator
   int values_to_copy;
//--- determine the number of values calculated in the indicator
   int calculated=BarsCalculated(handle);
   if(calculated<=0)
     {
      PrintFormat("BarsCalculated() returned %d, error code %d",calculated,GetLastError());
      return(0);
     }
//--- if it is the first start of calculation of the indicator or if the number of values in the iChaikin indicator changed
//---or if it is necessary to calculated the indicator for two or more bars (it means something has changed in the price history)
   if(prev_calculated==0 || calculated!=bars_calculated || rates_total>prev_calculated+1)
     {
      //--- if the iChaikinBuffer array is greater than the number of values in the iChaikin indicator for symbol/period, then we don't copy everything 
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
//--- fill the iChaikinBuffer array with values of the Chaikin Oscillator indicator
//--- if FillArrayFromBuffer returns false, it means the information is nor ready yet, quit operation
   if(!FillArrayFromBuffer(iChaikinBuffer,handle,values_to_copy)) return(0);
//--- form the message
   string comm=StringFormat("%s ==>  Updated value in the indicator %s: %d",
                            TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                            short_name,
                            values_to_copy);
//--- display the service message on the chart
   Comment(comm);
//--- memorize the number of values in the Chaikin Oscillator indicator
   bars_calculated=calculated;
//--- return the prev_calculated value for the next call
   return(rates_total);
  }
//+------------------------------------------------------------------+
//| Filling indicator buffers from the iChaikin indicator            |
//+------------------------------------------------------------------+
bool FillArrayFromBuffer(double &values[],  // indicator buffer of Chaikin Oscillator values
                         int ind_handle,    // handle of the iChaikin indicator
                         int amount         // number of copied values
                         )
  {
//--- reset error code
   ResetLastError();
//--- fill a part of the iChaikinBuffer array with values from the indicator buffer that has 0 index
   if(CopyBuffer(ind_handle,0,0,amount,values)<0)
     {
      //--- if the copying fails, tell the error code
      PrintFormat("Failed to copy data from the iChaikin indicator, error code %d",GetLastError());
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
